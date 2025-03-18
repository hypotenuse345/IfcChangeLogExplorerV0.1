import rdflib
from .item import Item
from typing import List

class TableRenderer:
    _css_1 = """
    <style>
    table {
    width: 100%;
    border-collapse: collapse;
    box-shadow: 0 0 20px rgba(0,0,0,0.15);
    border-radius: 12px; /* 确保圆角效果 */
    overflow: hidden;
    }
    th, td {
    padding: 12px 15px;
    text-align: left; /* 内容左对齐 */
    border-bottom: 1px solid #ddd;
    }
    th {
    background-color: rgba(25, 118, 210, 0.7); /* 使用带有透明度的蓝色背景 */
    color: white;
    font-weight: bold;
    backdrop-filter: blur(10px); /* 添加模糊效果 */
    }
    tr:nth-child(even) {
    background-color: #f2f2f2;
    }
    tr:hover {
    background-color: #eaeaea;
    }
    .tooltip {
    position: relative;
    display: inline-block;
    cursor: pointer;
    }
    .tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;
    position: absolute;
    z-index: 1;
    bottom: 125%; /* 在元素上方显示 */
    left: 50%;
    margin-left: -60px;
    opacity: 0;
    transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
    }
    </style>
    """

    _css_2 = """
    <style>
    table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #333;
    }
    th, td {
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid #ddd;
    }
    th {
    background-color: #f8f8f8;
    font-weight: bold;
    color: #555;
    }
    tbody tr:hover {
    background-color: #f5f5f5;
    }
    </style>
    """

    _css_3 = """
    <style>
    table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
    }
    th, td {
    text-align: left;
    padding: 16px 24px;
    border-bottom: 1px solid #e5e5e5;
    }
    th {
    background-color: #f8f8f8;
    color: #333;
    font-weight: 500;
    position: sticky;
    top: 0;
    z-index: 1;
    border-top: 1px solid #ddd;
    }
    tbody tr:nth-child(even) {
    background-color: #fafafa;
    }
    tbody tr:hover {
    background-color: #f0f0f0;
    }
    tbody tr:last-child td {
    border-bottom: none;
    }
    </style>
    """
    _create_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#308732" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus-square"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>"""
    _delete_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D32F2F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x-square"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>"""
    _edit_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>"""

    
    _html_content = """
<colgroup>
<col style="width: 40px;"/>
<col style="width: 20px;"/>
<col style="width: 20%;"/>
<col style="width: 20%;"/>
<col/>
</colgroup>
<thead>
<tr>
<th>({change_count})</th>
<th>Type</th>
<th>Entity ({entity_count})</th>
<th>Location</th>
<th>Description</th>
</tr>
</thead>
<tbody>"""
    
    _template = """
<tr>
<td data-label="#">{id}</td>
<td data-label="Type">{type}</td>
<td data-label="Entity">{entity}</td>
<td data-label="Location">{location}</td>
<td data-label="Description">{description}</td>
</tr>
    """

    def __init__(self, data: List[Item]):
        self.data = data

    def render(self, style_id:int=3):
        # Implement the rendering logic here
        if style_id not in [1,2,3]:
            style_id = 3
        style = getattr(self, f"_css_{style_id}")
        html_content = ""
        entities = set()
        for id, item in enumerate(self.data):
            html_content += self._template.format(
                id=id+1,
                type=item.type,
                entity=item.entity,
                location=item.location,
                description=item.description
            )
            entities.add(item.entity)
        html_content += "</tbody>"
        return style + self._html_content.format(entity_count=len(entities), change_count=len(self.data)) + html_content