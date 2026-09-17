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