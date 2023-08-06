import giossync
import time
import asyncio

class Test():

    def __init__(self, *args, **kwargs):
        self._client = giossync.GiosClient(552, timeout=10)
        self.uid = 552
        self.data = None
        self.location = None

    async def async_update(self):
        """Get the latest data and updates the states."""
        sensors = []
        res_sensors = await self._client.get_sensor_by_station_id(self.uid)
        for sensor in res_sensors:
            res_data = await self._client.get_sensor_data(sensor['id'])
            sensors.append({
                'id': sensor['id'],
                'name': sensor['param']['paramCode'],
                'value': res_data['values'][0]['value'],
                'date': res_data['values'][0]['date'],
            })
        self.data = sensors

    async def test(self):
        self.location = await self._client.get_location_data()



test = Test()
loop = asyncio.get_event_loop()
# task = loop.create_task(test.async_update())
# loop.run_until_complete(task)
# test.test()
task2 = loop.create_task(test.test())
loop.run_until_complete(task2)
# print(test.data)
print(test.location)


