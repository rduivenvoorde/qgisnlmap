import yaml
import psycopg2
import re


def run_query(q):
    conn = psycopg2.connect("dbname='osm' user='docker' host='localhost' password='docker' port='15432'")
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    conn.close()


def get_scale_denominator(zoom_lvl=0, dpi=90):
    return ((40000000 / 256) / (2**zoom_lvl)) * (2.54 / dpi)


def get_pixel_size(zoom_lvl):
    return (40000000 / 256) / (2**zoom_lvl)


def create_view(layer, schema='osm'):
    view_name = layer['id'].replace('-', '_')

    selection = layer['Datasource']['table']
    try:
        min_zoom = layer['properties']['minzoom']
    except(KeyError):
        min_zoom = 0
    scale_demoninator = get_scale_denominator(min_zoom)
    selection = selection.replace('!scale_denominator!', str(get_scale_denominator(zoom_lvl=min_zoom+1)))
    pixel_size = get_pixel_size(zoom_lvl=min_zoom+2)
    selection = selection.replace('!pixel_height!', str(pixel_size))
    selection = selection.replace('!pixel_width!', str(pixel_size))

    selection = re.sub('SELECT(\s+)way', 'SELECT osm_id, way', selection)

    first_bracket = selection.find('(') + 1
    last_bracket = selection.rfind(')')

    view_name = selection[last_bracket+1:]
    #print(view_name)
    view_name = view_name.replace('AS', '').strip()
    print(view_name)
    selection = selection[first_bracket:last_bracket]

    #print(selection)

    if view_name in ['icesheet_polygons', #no table icesheet_polygons
        'ocean_lz', #no table simplified_water_polygons
        'ocean', #no table water_polygons
        'icesheet_outlines', #no table icesheet_outlines
        'line_barriers', #bbox
        'turning_circle_sql', #bbox
        'roads_sql', #osm_id ambiguous
        'necountries', #no table ne_110m_admin_0_boundary_lines_land
        'country_names', #bbox
        'state_names', #bbox
        'stations', #bbox
        'junctions', #bbox
        'bridge_text', #bbox
        'county_names', #bbox
        'amenity_points', #bbox
        'roads_text_ref_low_zoom', #osm_id ambiguous
        'roads_area_text_name', #bbox
        'text_poly_low_zoom', #bbox
        'building_text', #bbox
        'addresses', #bbox
        'amenity_low_priority', #bbox
    ]:
        return

    q = f'DROP VIEW IF EXISTS "{schema}"."view_{view_name}";'
    #print(q)
    run_query(q)

    q = f'CREATE VIEW "{schema}"."view_{view_name}" AS {selection};'
    #print(q)
    run_query(q)

run_query('''DROP SCHEMA IF EXISTS "osm" CASCADE;''')
run_query('''CREATE SCHEMA "osm";''')

carto_project_fn = '../openstreetmap-carto/project.mml'

with open(carto_project_fn, 'r') as project_file:
    project_dict = yaml.safe_load(project_file)

#style_sheets = project_dict['Stylesheet']

for layer in project_dict['Layer']:
    create_view(layer)
