class HTMLNode:
	def __init__(self, tag=None, value=None, children: list | None = None, props: dict | None = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("Not yet implemented")
	
	def props_to_html(self):
		result = ""
		if self.props is None:
			return result
		for key, value in self.props.items():
			html = f' {key}="{value}"'
			result += html
		return result
		
	def __repr__(self):
		return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props as html: {self.props_to_html()}"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, children=None, props=props)

	def to_html(self):
		if self.value is None:
			raise ValueError(f"LeafNode has no value: {self}")
		if not self.tag:
			return (self.value)
		if self.props:
			return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
		return f"<{self.tag}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"tag: {self.tag}, value: {self.value}, props as html: {self.props_to_html()}"

class ParentNode(HTMLNode):
	def __init__(self, tag, children: list[HTMLNode], props=None):
		super().__init__(tag, value=None, children=children, props=props)

	def to_html(self):
		if not self.tag:
			raise ValueError
		if not self.children:
			raise ValueError("No children found")
		children_results = []
		for child in self.children:
			children_results.append(child.to_html())
		if self.props:
			return f'<{self.tag}{self.props_to_html()}>{"".join(children_results)}</{self.tag}>'
		return f"<{self.tag}>{"".join(children_results)}</{self.tag}>"

	def __repr__(self):
		return f"tag: {self.tag}, children: {self.children}, props as html: {self.props_to_html()}"