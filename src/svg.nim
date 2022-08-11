import 
  std/[
    strformat,
    strutils,
    sugar
  ]

type SvgAttribute = tuple[name: string, value: string]

proc newSvgAttribute*(name, value: string): SvgAttribute =
  result.name = name
  result.value = value

type SvgKind* = enum
  Circle, Ellipse, Line, Path, Rect, Text, Title

type SvgNode = ref object
  kind: SvgKind
  attrs: seq[SvgAttribute]
  children: seq[SvgNode]
  inner: string

proc newSvgNode*(kind: SvgKind, children: seq[SvgNode] = @[], attrs: seq[SvgAttribute] = @[], inner: string = ""): SvgNode =
  SvgNode(kind: kind, children: children, attrs: attrs, inner: inner)

proc add*(node: SvgNode, child: SvgNode) =
  node.children.add(child)

proc set*(node: SvgNode, name, value: string): void =
  node.attrs.add(newSvgAttribute(name, value))

proc `$`*(node: SvgNode): string =
  let 
    nk = toLower($node.kind)

    attrs = " " & collect(
      for attr in node.attrs:
        let val = attr.value.replace("\"", "")
        &"{attr.name}=\"{val}\""
    ).join(" ")

  var children: string
  if node.children.len != 0:
    children = collect(
      for child in node.children:
        $child
    ).join(" ")
  else:
    children = node.inner

  if attrs == " ":
    &"<{nk}>{children}</{nk}>"
  else:
    &"<{nk}{attrs}>{children}</{nk}>"

type Svg* = ref object
  width, height: int
  children: seq[SvgNode]

proc newSvg*(width, height: int, children: seq[SvgNode] = @[]): Svg =
  Svg(width: width, height: height, children: children)

proc add*(svg: Svg, child: SvgNode) =
  svg.children.add(child)

proc `$`*(svg: Svg): string =
  let
    height = svg.height
    width = svg.width
    children = collect(
      for child in svg.children:
        $child
    ).join("\n")
  &"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">{children}</svg>"

proc write*(svg: Svg, filename: string): void =
  writeFile(fmt"./assets/{filename}.svg", $svg)