#!/usr/bin/env python3
"""Convert Umlet .uxf diagrams into Mermaid markdown files."""

from __future__ import annotations

import html
import pathlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Tuple

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
UML_DIR = BASE_DIR / "_files" / "uml"


@dataclass
class Element:
    kind: str
    text: str
    coords: Tuple[float, float, float, float]
    extras: str


def parse_elements(path: pathlib.Path) -> List[Element]:
    root = ET.parse(path).getroot()
    elements: List[Element] = []
    for elem in root.findall(".//element"):
        kind = elem.findtext("id", default="")
        text = html.unescape(elem.findtext("panel_attributes", default="")).strip("\n")
        coords_node = elem.find("coordinates")
        if coords_node is None:
            continue
        coords = tuple(
            float(coords_node.findtext(tag, default="0"))
            for tag in ("x", "y", "w", "h")
        )
        extras = html.unescape(elem.findtext("additional_attributes", default=""))
        elements.append(Element(kind=kind, text=text, coords=coords, extras=extras))
    return elements


def normalize_name(raw: str) -> str:
    return " ".join(raw.split())


def list_participants(elements: List[Element]) -> Dict[str, float]:
    centers: Dict[str, Tuple[float, float]] = {}
    for elem in elements:
        if elem.kind != "UMLGeneric":
            continue
        text = normalize_name(elem.text)
        if not text or "=" in text:
            continue
        x, _y, w, _h = elem.coords
        center_x = x + w / 2.0
        if text not in centers or elem.coords[1] < centers[text][1]:
            centers[text] = (center_x, elem.coords[1])
    return {name: center for name, (center, _y) in centers.items()}


def parse_polyline_points(elem: Element) -> List[Tuple[float, float]]:
    values = [v for v in elem.extras.split(";") if v]
    if len(values) < 4:
        return []
    pts = []
    for i in range(0, len(values), 2):
        try:
            local_x = float(values[i])
            local_y = float(values[i + 1])
        except (IndexError, ValueError):
            break
        abs_x = elem.coords[0] + local_x
        abs_y = elem.coords[1] + local_y
        pts.append((abs_x, abs_y))
    return pts


def closest_participant(
    participants: Dict[str, float],
    boxes: Dict[str, Tuple[float, float, float, float]] | None,
    point: Tuple[float, float],
) -> str | None:
    if boxes:
        px, py = point
        for name, (x, y, w, h) in boxes.items():
            if (x - 5) <= px <= (x + w + 5) and (y - 5) <= py <= (y + h + 5):
                return name
    if not participants:
        return None
    px = point[0]
    return min(participants, key=lambda name: abs(participants[name] - px))


def relation_edges(
    elements: List[Element],
    participants: Dict[str, float],
    boxes: Dict[str, Tuple[float, float, float, float]] | None = None,
    require_label: bool = False,
) -> List[Tuple[str, str, str]]:
    edges: List[Tuple[str, str, str]] = []
    for elem in elements:
        if elem.kind != "Relation":
            continue
        text_lines = [line for line in elem.text.splitlines() if line]
        if len(text_lines) < 2 and require_label:
            continue
        label = text_lines[1].strip() if len(text_lines) > 1 else ""
        points = parse_polyline_points(elem)
        if len(points) < 2:
            continue
        head_point = points[0]
        tail_point = points[-1]
        sender = closest_participant(participants, boxes, tail_point)
        receiver = closest_participant(participants, boxes, head_point)
        if not sender or not receiver or sender == receiver:
            continue
        edges.append((sender, receiver, label))
    return edges


def convert_sequence(elements: List[Element], target: pathlib.Path) -> None:
    participants = list_participants(elements)
    lines = ["sequenceDiagram"]
    for name in sorted(participants, key=lambda n: participants[n]):
        safe = name.replace(" ", "_")
        lines.append(f"    participant {safe} as {name}")
    for sender, receiver, label in relation_edges(elements, participants, None):
        safe_sender = sender.replace(" ", "_")
        safe_receiver = receiver.replace(" ", "_")
        pretty_label = label.replace("\\", " ")
        lines.append(f"    {safe_sender}->>{safe_receiver}: {pretty_label}")
    body = "\n".join(lines)
    target.write_text(f"```mermaid\n{body}\n```\n", encoding="utf-8")


def mermaid_id(raw: str) -> str:
    clean = "".join(ch if ch.isalnum() else "_" for ch in raw)
    clean = clean.strip("_") or "Class"
    if clean[0].isdigit():
        clean = f"_{clean}"
    return clean


def parse_class(elem: Element) -> Tuple[str, List[str]]:
    raw_lines = [line.rstrip("\r") for line in elem.text.splitlines()]
    header: List[str] = []
    body: List[str] = []
    before_body = True
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "--":
            before_body = False
            continue
        if before_body:
            header.append(line)
        else:
            body.append(line)
    if not header:
        name = "Unnamed"
        metadata: List[str] = []
    else:
        name = normalize_name(header[-1])
        metadata = header[:-1]
    members: List[str] = [f"%% {normalize_name(meta)}" for meta in metadata]
    members.extend(body)
    return name, members


def convert_class_diagram(elements: List[Element], target: pathlib.Path) -> None:
    class_elems = [elem for elem in elements if elem.kind == "UMLClass"]
    classes = [parse_class(elem) for elem in class_elems]
    participants = {
        name: elem.coords[0] + elem.coords[2] / 2.0
        for elem, (name, _members) in zip(class_elems, classes)
    }
    boxes = {name: elem.coords for elem, (name, _members) in zip(class_elems, classes)}
    edges = relation_edges(elements, participants, boxes)
    lines = ["classDiagram"]
    for name, members in classes:
        safe = mermaid_id(name)
        lines.append(f"    class {safe}[\"{name}\"] {{")
        for member in members:
            lines.append(f"        {member}")
        lines.append("    }")
    for sender, receiver, label in edges:
        safe_sender = mermaid_id(sender)
        safe_receiver = mermaid_id(receiver)
        lines.append(f"    {safe_sender} -- {safe_receiver}: {label}")
    body = "\n".join(lines)
    target.write_text(f"```mermaid\n{body}\n```\n", encoding="utf-8")


def main() -> None:
    for uxf in UML_DIR.glob("*.uxf"):
        elements = parse_elements(uxf)
        target = uxf.with_suffix(".md")
        if any(elem.kind == "UMLClass" for elem in elements):
            convert_class_diagram(elements, target)
        else:
            convert_sequence(elements, target)


if __name__ == "__main__":
    main()
