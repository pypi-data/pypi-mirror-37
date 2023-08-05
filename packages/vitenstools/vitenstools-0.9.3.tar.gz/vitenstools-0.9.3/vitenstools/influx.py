try:
    import influxdb
    import piwebapi
except:
    pass


def write_softsensor(self, value):

    if'Monsterpuntcode' in self.children:
        puntcode = self.children['Monsterpuntcode'].value
    else:
        puntcode = piwebapi.Attribute(self.links['Parent']).children['Monsterpuntcode'].value

    if '_SS' not in puntcode:
        raise ValueError('Dit is geen softsensor')

    analyte = self.children['Analyte'].value
    testcode = self.children['Testcode'].value

    influx_json = []
    influx_json.append({
        "measurement": puntcode,
        "tags": {
            "testcode": testcode,
            "analyte": analyte
            },
        "fields": {
            "value": value
            }
        })

    client = influxdb.InfluxDBClient(database='slimm')
    client.write_points(influx_json)


piwebapi.Attribute.write_softsensor = write_softsensor
