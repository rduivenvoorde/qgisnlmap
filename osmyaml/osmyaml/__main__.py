import click
import yaml
import re

@click.command()
def hello():
    click.echo('Hello World!')

@click.command()
@click.option('-q', '--without_query', default=False, is_flag=True, help='Do NOT print queries')
def load_osm_yaml(without_query:bool):
    with open("./osm.yaml", mode="rt", encoding="utf-8") as file:
        osmyaml = yaml.safe_load(file)
        #print(osmyaml)
        for layer in osmyaml["Layer"]:
            layer_id = layer["id"]
            print(f'\n-- {layer_id}  -  {layer["properties"]}')
            if not without_query:
                # on one line
                #query = layer["Datasource"]["table"].replace("\n", "")
                # trying to replace 'SELECT   way' with 'SELECT oms_id, wayd'
                query = layer["Datasource"]["table"]
                query = re.sub('SELECT(\s+)way', 'SELECT osm_id, way', query)
                # replace the 'AS layerid' part
                # NOT working as layer_id is NOT the same as the AS string...
                # reg = f'AS {layer_id}'.replace('-', '_')
                # query = re.sub(reg, '', query)
                print(f'{query}')


if __name__ == '__main__':
    #hello()
    load_osm_yaml()

