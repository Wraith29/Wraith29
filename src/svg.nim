import 
  std/[
    strformat,
    strutils,
    sugar
  ],
  class

type SvgAttribute = tuple[name: string, value: string]

proc newSvgAttribute*(name, value: string): SvgAttribute =
  result.name = name
  result.value = value

type SvgKind* = enum
  Circle, Ellipse, Line, Path, Rect, Text, Title

class SvgNode:
  kind: SvgKind
  attrs: seq[SvgAttribute]
  children: seq[SvgNode]
  inner: string

  func newSvgNode*(kind: SvgKind, children: seq[SvgNode] = @[], attrs: seq[SvgAttribute] = @[], inner: string = ""): SvgNode {.static.} =
    SvgNode(kind: kind, children: children, attrs: attrs, inner: inner)

  func add*(self: SvgNode, child: SvgNode) =
    self.children.add(child)
  
  func set*(self: SvgNode, name, value: string) =
    self.attrs.add(newSvgAttribute(name, value))
  
  func `$`*(self): string =
    let 
      nk = toLower($self.kind)

      attrs = " " & collect(
        for attr in self.attrs:
          let val = attr.value.replace("\"", "")
          &"{attr.name}=\"{val}\""
      ).join(" ")

    var children: string
    if self.children.len != 0:
      children = collect(
        for child in self.children:
          $child
      ).join(" ")
    else:
      children = self.inner

    if attrs == " ":
      &"<{nk}>{children}</{nk}>"
    else:
      &"<{nk}{attrs}>{children}</{nk}>"

class Svg:
  width: int
  height: int
  children: seq[SvgNode]

  proc newSvg*(width, height: int, children: seq[SvgNode] = @[]): Svg {.static.}=
    Svg(width: width, height: height, children: children)

  proc add*(self: Svg, child: SvgNode) =
    self.children.add(child)

  proc `$`*(self: Svg): string =
    let
      height = self.height
      width = self.width
      children = collect(
        for child in self.children:
          $child
      ).join("\n")
    &"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">{children}</svg>"

  proc write*(self: Svg, filename: string) =
    writeFile(fmt"./assets/{filename}.svg", $self)