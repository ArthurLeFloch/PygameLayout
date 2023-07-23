from pygame_ui_controls import *
from lxml import etree

def parse_margin(node):
    default = node.get('margin', 0)

    top = node.get('margin_top', default)
    right = node.get('margin_right', default)
    bottom = node.get('margin_bottom', default)
    left = node.get('margin_left', default)

    return [int(top), int(right), int(bottom), int(left)]

def parse_border_radius(node):
    default = node.get('border_radius', 0)

    top_left = node.get('border_radius_top_left', default)
    top_right = node.get('border_radius_top_right', default)
    bottom_right = node.get('border_radius_bottom_right', default)
    bottom_left = node.get('border_radius_bottom_left', default)

    return [int(top_left), int(top_right), int(bottom_right), int(bottom_left)]

def compute_bounds(cache, node, parent_bounds):
    parent_x, parent_y, parent_end_x, parent_end_y = parent_bounds
    parent_width = parent_end_x - parent_x
    parent_height = parent_end_y - parent_y

    x, y, w, h = 0, 0, 0, 0
    width, height = node.get('width', '0'), node.get('height', '0')
    m_top, m_right, m_bottom, m_left = parse_margin(node)

    min_x = parent_x
    max_x = parent_x + parent_width
    if 'start_to_start_of' in node.attrib:
        min_x = cache[node.attrib['start_to_start_of']][0]
    if 'start_to_end_of' in node.attrib:
        min_x = cache[node.attrib['start_to_end_of']][2]
    if 'end_to_start_of' in node.attrib:
        max_x = cache[node.attrib['end_to_start_of']][0]
    if 'end_to_end_of' in node.attrib:
        max_x = cache[node.attrib['end_to_end_of']][2]
    min_x += m_left
    max_x -= m_right

    if width == "match_parent":
        w = parent_width - m_left - m_right
        x = parent_x + m_left
    elif width == '0':
        w = max_x - min_x
        x = min_x
    else:
        if width[-1] == '%':
            w = int(width[:-1].strip()) * parent_width // 100 - m_left - m_right
        else:
            w = int(width)
            
        if (('end_to_end_of' in node.attrib) or ('end_to_start_of' in node.attrib)):
            x = max_x - w
        else:
            x = min_x

    min_y = parent_y
    max_y = parent_y + parent_height
    if 'top_to_top_of' in node.attrib:
        min_y = cache[node.attrib['top_to_top_of']][1]
    if 'top_to_bottom_of' in node.attrib:
        min_y = cache[node.attrib['top_to_bottom_of']][3]
    if 'bottom_to_top_of' in node.attrib:
        max_y = cache[node.attrib['bottom_to_top_of']][1]
    if 'bottom_to_bottom_of' in node.attrib:
        max_y = cache[node.attrib['bottom_to_bottom_of']][3]
    min_y += m_top
    max_y -= m_bottom

    if height == "match_parent":
        h = parent_height - m_top - m_bottom
        y = parent_y + m_top
    elif height == '0':
        h = max_y - min_y
        y = min_y
    else:
        if height[-1] == '%':
            h = int(height[:-1].strip()) * parent_height // 100 - m_top - m_bottom
        else:
            h = int(height)
        
        if (('bottom_to_bottom_of' in node.attrib) or ('bottom_to_top_of' in node.attrib)):
            y = max_y - h
        else:
            y = min_y
    
    if node.tag == 'CheckBox' and h != w:
        size = min(h, w)
        h, w = size, size

    if 'id' in node.attrib:
        cache[node.attrib['id']] = [x - m_left, y - m_top, x + w + m_right, y + h + m_bottom]

    return [x, y, x + w, y + h]

def compute_text_pos(gravity, text, bounds):
    x, y, end_x, end_y = bounds
    width, height = end_x - x, end_y - y
    text_x, text_y = x, y

    rendered = UI.FONT.render(text, "black")[0]
    text_width, text_height = rendered.get_size()

    if gravity == 'top_right':
        text_x = x + width - text_width
    elif gravity == 'top_center':
        text_x = x + (width - text_width) // 2
    elif gravity == 'top_left':
        text_x = end_x - text_width
    elif gravity == 'left_center':
        text_y = y + (height - text_height) // 2
    elif gravity == 'center':
        text_x = x + (width - text_width) // 2
        text_y = y + (height - text_height) // 2
    elif gravity == 'right_center':
        text_x = end_x - text_width
        text_y = y + (height - text_height) // 2
    elif gravity == 'bottom_left':
        text_y = end_y - text_height
    elif gravity == 'bottom_center':
        text_x = x + (width - text_width) // 2
        text_y = end_y - text_height
    elif gravity == 'bottom_right':
        text_x = end_x - text_width
        text_y = end_y - text_height

    return text_x, text_y


class Layout:
    
    def set_font(font_file):
        # TODO: add font size, fonts cache
        UI.FONT = pygame.freetype.Font(font_file, 24)
    
    def __init__(self, xml_file, screen_size):
        self.views = {}
        self.screen_size = screen_size
        self.data = [] # Erased on resize
        self.permanent_data = {}
        self.set_source(xml_file)
    
    def set_source(self, xml_file):
        self.file = xml_file
        self.root = etree.parse(xml_file).getroot()
        UI.delete_all()
        View.dict = {}
        self.create_ui_components()
        self.resize(self.screen_size)

    ############
    #  RESIZE  #
    ############
    def resize_rec(self, node, pos, size):
        parent_x, parent_y = pos
        parent_width, parent_height = size
    
        cache = {'parent': [parent_x, parent_y, parent_x + parent_width, parent_y + parent_height]}
        current_data = []

        for child in node:
            id = child.get('id', 'none')
            x, y, end_x, end_y = compute_bounds(cache, child, cache['parent'])
            width = end_x - x
            height = end_y - y

            node_data = {'type': child.tag, 'id': id, 'pos': (x, y), 'size': (width, height), 'border_radius': parse_border_radius(child), 'color': child.get('color', 'none')}

            if child.tag == 'Text':
                text = child.get('text', '')
                if id != 'none':
                    self.permanent_data[id]['parent_bounds'] = (x, y, end_x, end_y)
                    text = Text.get_text(id)
                node_data['text_pos'] = compute_text_pos(child.get('gravity', 'top_left'), text, (x, y, end_x, end_y))
                Text.set_pos(id, node_data['text_pos'])
            elif child.tag == 'Button':
                Button.set_pos(id, (x, y))
                Button.set_size(id, (width, height))
            elif child.tag == 'ImageButton':
                ImageButton.set_pos(id, (x, y))
                ImageButton.set_size(id, (width, height))
            elif child.tag == 'Slider':
                Slider.set_pos(id, (x, y))
                Slider.set_size(id, (width, height))
            elif child.tag == 'CheckBox':
                CheckBox.set_pos(id, (x, y))
                size = min(width, height)
                CheckBox.set_size(id, (size, size))
                node_data['size'] = (size, size)
            elif child.tag == 'View':
                View.set_pos(id, (x, y))
                View.set_size(id, (width, height))
            current_data.append(node_data)
        
        self.data += current_data
    
        for node_data, child in zip(current_data, node):
            x, y, width, height = node_data['pos'] + node_data['size']
            self.resize_rec(child, (x, y), (width, height))

    def resize(self, size):
        self.screen_size = size
        self.data = []
        self.data.append({'type': self.root.tag, 'pos': (0, 0), 'size': size, 'border_radius': (0, 0, 0, 0), 'color': self.root.get('color', 'none')})
        self.resize_rec(self.root, (0, 0), size)

    #######################
    #  CREATE COMPONENTS  #
    #######################
    def create_ui_components_rec(self, node):
        for child in node:
            id = child.get('id', None)
            pos = (0, 0)
            size = (50, 50)

            permanent = {}

            if child.tag == 'Text':
                Text(id, pos, child.get('text', ''), child.get('text_color', '#000000'))
                if 'gravity' in child.attrib:
                    permanent['gravity'] = child.attrib['gravity']
            elif child.tag == 'Button':
                locked = child.get('locked', 'false') == 'true'
                hoverable = child.get('hoverable', 'true') == 'true'
                Button(id, pos, text=child.get('text', ''), hoverable=hoverable, locked=locked)
            elif child.tag == 'ImageButton':
                locked = child.get('locked', 'false') == 'true'
                hoverable = child.get('hoverable', 'true') == 'true'
                ImageButton(id, child.get('src'), pos, hoverable=hoverable, locked=locked)
            elif child.tag == 'Slider':
                value = int(child.get('value', '7'))
                mini = int(child.get('min', '0'))
                maxi = int(child.get('max', '10'))
                ticks = int(child.get('ticks', '0'))
                locked = child.get('locked', 'false') == 'true'
                hoverable = child.get('hoverable', 'true') == 'true'
                Slider(id, pos, size, hoverable=hoverable, locked=locked, value=value, range=(mini, maxi), ticks=ticks)
            elif child.tag == 'CheckBox':
                checked = child.get('checked', 'false') == 'true'
                locked = child.get('locked', 'false') == 'true'
                hoverable = child.get('hoverable', 'true') == 'true'
                others = child.get('link', 'none')
                linked = None
                if others != 'none':
                    linked = others.split(',')
                CheckBox(id, pos, checked=checked, hoverable=hoverable, locked=locked, linked=linked)
            elif child.tag == 'View':
                View(id)
            elif child.tag != 'Layout':
                raise Exception(f"Unknown tag: {child.tag}")

            if id != 'none':
                self.permanent_data[id] = permanent

            self.create_ui_components_rec(child)

    def create_ui_components(self):
        self.create_ui_components_rec(self.root)
    
    ############
    #  UPDATE  #
    ############
    def apply_background_color(self, screen, pos, size, color, border_radius):
        if color != 'none':
            b_top_left, b_top_right, b_bottom_right, b_bottom_left = border_radius
            pygame.draw.rect(screen, color, (*pos, *size), border_top_left_radius=b_top_left, border_top_right_radius=b_top_right, border_bottom_right_radius=b_bottom_right, border_bottom_left_radius=b_bottom_left)

    def update(self, screen):
        for node in self.data:
            #node_type = node['type']
            self.apply_background_color(screen, node['pos'], node['size'], node['color'], node['border_radius'])
        
        UI.update(screen, *pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
    
    #############
    #  GETTERS  #
    #############
    def get_text(self, id):
        return Text.get_text(id)
    
    def get_value(self, id):
        return Slider.get_value(id)

    def is_checked(self, id):
        return CheckBox.checked(id)

    #############
    #  SETTERS  #
    #############
    def set_on_click(self, id, callback):
        def ui_callback():
            callback(self)
        Button.set_on_click(id, ui_callback)
    
    def set_on_image_click(self, id, callback):
        def ui_callback():
            callback(self)
        ImageButton.set_on_click(id, ui_callback)
    
    def set_text(self, id, text):
        Text.set_text(id, text)
        if id in self.permanent_data:
            if 'gravity' in self.permanent_data[id]:
                Text.set_pos(id, compute_text_pos(self.permanent_data[id]['gravity'], text, self.permanent_data[id]['parent_bounds']))
    
    def set_on_value_changed(self, id, callback):
        def ui_callback(value):
            callback(self, value)
        Slider.set_on_value_changed(id, ui_callback)
    
    def set_on_view_update(self, id, callback):
        View.set_on_screen_update(id, callback)
    
    def set_on_action(self, id, callback):
        def ui_callback(value):
            callback(self, value)
        CheckBox.set_on_action(id, ui_callback)