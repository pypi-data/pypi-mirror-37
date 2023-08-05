# coding=utf-8
"""
Manages mission objects
"""
# pylint: skip-file
# FIXME: pylint the shit out of this
import calendar
import typing
from itertools import chain
from time import gmtime, strftime

from elib_miz import LOGGER
from elib_miz.validator import VALID_BOOL, VALID_FLOAT, VALID_INT, VALID_POSITIVE_INT, VALID_STR, Validator

EPOCH_DELTA = 1306886400

validator_group_or_unit_name = Validator(_type=str, _regex=r'[a-zA-Z0-9\_\-\#]+',
                                         exc=ValueError, logger=LOGGER)


class BaseMissionObject:
    """
    Serves as base mission (dictionary) object
    """

    def __init__(self, mission_dict: dict, l10n: dict) -> None:
        super().__init__()

        if not isinstance(mission_dict, dict):
            raise TypeError('mission_dict should be an dict, got: {}'.format(type(mission_dict)))

        if not isinstance(l10n, dict):
            raise TypeError('l10n should be an dict, got: {}'.format(type(l10n)))

        self.d = mission_dict
        self.l10n = l10n

        self.weather = None
        self._blue_coa = None
        self._red_coa = None
        self.ground_control = None

        self._countries_by_name: typing.Dict[str, 'Country'] = {}
        self._countries_by_id: typing.Dict[int, 'Country'] = {}

    def get_country_by_name(self, country_name: str) -> typing.Optional['Country']:
        """
        Gets a country from its name

        Args:
            country_name: country name

        Returns: Country
        """
        VALID_STR.validate(country_name, 'get_country_by_name', exc=ValueError)
        if country_name not in self._countries_by_name.keys():
            for country in self.countries:

                if country.country_name == country_name:
                    self._countries_by_name[country_name] = country
                    return country
            raise ValueError(country_name)
        else:
            return self._countries_by_name[country_name]

    def get_country_by_id(self, country_id: int) -> typing.Optional['Country']:
        """
        Gets a country from its name

        Args:
            country_id: country id

        Returns: Country
        """
        VALID_POSITIVE_INT.validate(country_id, 'get_country_by_id')
        if country_id not in self._countries_by_id.keys():
            for country in self.countries:

                if country.country_id == country_id:
                    self._countries_by_id[country_id] = country
                    return country
            raise ValueError(country_id)
        else:
            return self._countries_by_id[country_id]

    def get_groups_from_category(self, category: str) -> typing.Iterator['Group']:
        """
        Gets all groups from a category

        Args:
            category: category

        Returns: generator of Groups
        """
        Mission.validator_group_category.validate(category, 'get_groups_from_category')
        for group in self.groups:
            if group.group_category == category:
                yield group

    def get_units_from_category(self, category: str) -> typing.Iterator['BaseUnit']:
        """
        Gets all units from a category

        Args:
            category: category

        Returns: generator of BaseUnit
        """
        Mission.validator_group_category.validate(category, 'get_units_from_category')
        for unit in self.units:
            if unit.group_category == category:
                yield unit

    def get_group_by_id(self, group_id: str) -> typing.Optional['Group']:
        """
        Gets a group by id

        Args:
            group_id: group id

        Returns: Group
        """
        VALID_POSITIVE_INT.validate(group_id, 'get_group_by_id', exc=ValueError)
        for group in self.groups:

            if group.group_id == group_id:
                return group
        return None

    def get_clients_groups(self) -> typing.Iterator['Group']:
        """
        Gets all clients groups

        Returns: generator of Groups
        """
        for group in self.groups:

            if group.group_is_client_group:
                yield group

    def get_group_by_name(self, group_name: str) -> typing.Optional['Group']:
        """
        Gets a group from its name

        Args:
            group_name:

        Returns: Group
        """
        VALID_STR.validate(group_name, 'get_group_by_name')
        for group in self.groups:

            if group.group_name == group_name:
                return group
        return None

    def get_unit_by_name(self, unit_name: str) -> typing.Optional['BaseUnit']:
        """
        Gets a unit from its name

        Args:
            unit_name: unit name

        Returns:
        """
        VALID_STR.validate(unit_name, 'get_unit_by_name')
        for unit in self.units:

            if unit.unit_name == unit_name:
                return unit
        return None

    def get_unit_by_id(self, unit_id: str) -> typing.Optional['BaseUnit']:
        """
        Gets a unit from its ID

        Args:
            unit_id: unit id

        Returns: Unit
        """
        VALID_POSITIVE_INT.validate(unit_id, 'get_unit_by_id')
        for unit in self.units:

            if unit.unit_id == unit_id:
                return unit
        return None

    @property
    def units(self) -> typing.Iterator['BaseUnit']:
        """
        Iterates over all units

        Returns: generator of Unit
        """
        for group in self.groups:
            for unit in group.units:

                yield unit

    @property
    def groups(self) -> typing.Iterator['Group']:
        """
        Iterates over all groups

        Returns: generator of Group
        """
        for country in self.countries:
            for group in country.groups:

                yield group

    @property
    def next_group_id(self) -> int:
        """
        Returns: next free GroupId
        """
        ids: typing.Set[int] = set()
        for group in chain(self._blue_coa.groups, self._red_coa.groups):  # type: ignore

            id_ = group.group_id
            if id_ in ids:
                raise IndexError(group.group_name)
            ids.add(id_)
        return max(ids) + 1

    @property
    def next_unit_id(self) -> int:
        """
        Returns: next free Unit ID
        """
        ids: typing.Set[int] = set()
        for unit in chain(self._blue_coa.units, self._red_coa.units):  # type: ignore

            id_ = unit.unit_id
            if id_ in ids:
                raise IndexError(unit.unit_name)
            ids.add(id_)
        return max(ids) + 1

    @property
    def coalitions(self) -> typing.Iterator['Coalition']:
        """
        Returns: generator over all coalitions
        """
        for coalition in [self._blue_coa, self._red_coa]:

            yield coalition  # type: ignore

    @property
    def countries(self) -> typing.Iterator['Country']:
        """
        Returns: generator over all countries
        """
        for coalition in self.coalitions:
            for country in coalition.countries:

                yield country

    @property
    def _section_date(self):
        return self.d['date']

    @property
    def second(self) -> int:
        gm_time = gmtime(self.mission_start_time)
        return gm_time.tm_sec

    @second.setter
    def second(self, value: int):
        Mission.validator_minute_second.validate(value, 'second')
        gm_time = gmtime(self.mission_start_time)
        self.mission_start_time = calendar.timegm(
            (gm_time.tm_year, gm_time.tm_mon, gm_time.tm_mday, gm_time.tm_hour, gm_time.tm_min, value))

    @property
    def minute(self) -> int:
        gm_time = gmtime(self.mission_start_time)
        return gm_time.tm_min

    @minute.setter
    def minute(self, value: int):
        Mission.validator_minute_second.validate(value, 'minute')
        gm_time = gmtime(self.mission_start_time)
        self.mission_start_time = calendar.timegm(
            (gm_time.tm_year, gm_time.tm_mon, gm_time.tm_mday, gm_time.tm_hour, value, gm_time.tm_sec))

    @property
    def hour(self) -> int:
        gm_time = gmtime(self.mission_start_time)
        return gm_time.tm_hour

    @hour.setter
    def hour(self, value: int):
        Mission.validator_hour.validate(value, 'hour')
        gm_time = gmtime(self.mission_start_time)
        self.mission_start_time = calendar.timegm(
            (gm_time.tm_year, gm_time.tm_mon, gm_time.tm_mday, value, gm_time.tm_min, gm_time.tm_sec))

    @property
    def day(self) -> int:
        """
        Returns: return "day" part of the mission start time
        """
        return self._section_date['Day']

    @day.setter
    def day(self, value: int):
        Mission.validator_day.validate(value, 'day')
        # Get the last day of the current month
        self._section_date['Day'] = min(value, calendar.monthrange(self.year, self.month)[1])

    @property
    def month(self) -> int:
        """
        Returns: return "month" part of the mission start time
        """
        return self._section_date['Month']

    @month.setter
    def month(self, value: int):
        Mission.validator_month.validate(value, 'month')
        self._section_date['Month'] = value
        self.day = self.day  # update day (for max value)

    @property
    def year(self) -> int:
        """
        Returns: return "year" part of the mission start time
        """
        return self._section_date['Year']

    @year.setter
    def year(self, value: int):
        Mission.validator_year.validate(value, 'year')
        self._section_date['Year'] = value
        self.day = self.day  # update day (for max value)

    @property
    def mission_start_time(self) -> int:
        """
        Returns: raw mission start time
        """
        return self.d['start_time']

    @mission_start_time.setter
    def mission_start_time(self, value):
        Mission.validator_start_time.validate(value, 'start_time')
        self.d['start_time'] = value

    @staticmethod
    def _start_time_as_string(start_time):
        return strftime('%H:%M:%S', gmtime(start_time))

    @staticmethod
    def _start_date_as_string(day, month, year):
        return strftime(f'{day:02}/{month:02}/{year}')

    def _start_datetime_as_string(self, startime):
        return f'{self.mission_start_date_as_string} {self._start_time_as_string(startime)}'

    @property
    def mission_start_time_as_string(self) -> str:
        """
        Returns: mission start time as string
        """
        return self._start_time_as_string(self.mission_start_time)

    @property
    def mission_start_date_as_string(self) -> str:
        """
        Returns: mission start date as string
        """
        return self._start_date_as_string(self.day, self.month, self.year)

    @property
    def mission_start_datetime_as_string(self) -> str:
        """
        Returns: mission start time and date as string
        """
        return f'{self.mission_start_date_as_string} {self.mission_start_time_as_string}'

    @property
    def _sortie_name_key(self):
        return self.d['sortie']

    @property
    def sortie_name(self):
        """
        Returns: sortie name
        """
        return self.l10n[self._sortie_name_key]

    @sortie_name.setter
    def sortie_name(self, value):
        VALID_STR.validate(value, 'sortie name')
        self.l10n[self._sortie_name_key] = value


class Mission(BaseMissionObject):
    """
    Represents a Mission object
    """
    validator_start_time = Validator(
        _type=int,
        _min=0,
        _max=86399,
        exc=ValueError,
        logger=LOGGER
    )
    validator_year = Validator(
        _type=int,
        _min=1900,
        _max=2100,
        exc=ValueError,
        logger=LOGGER
    )
    validator_month = Validator(
        _type=int,
        _min=1,
        _max=12,
        exc=ValueError,
        logger=LOGGER
    )
    validator_day = Validator(
        _type=int,
        _min=1,
        _max=31,
        exc=ValueError,
        logger=LOGGER
    )
    validator_hour = Validator(
        _type=int,
        _min=0,
        _max=23,
        exc=ValueError,
        logger=LOGGER
    )
    validator_minute_second = Validator(
        _type=int,
        _min=0,
        _max=59,
        exc=ValueError,
        logger=LOGGER
    )
    validator_heading = Validator(
        _type=int,
        _min=0,
        _max=359,
        exc=ValueError,
        logger=LOGGER
    )
    validator_group_category = Validator(
        _type=str,
        _in_list=['helicopter', 'ship', 'plane', 'vehicle'],
        exc=ValueError,
        logger=LOGGER)
    valid_group_categories = ('helicopter', 'plane', 'ship', 'vehicle')

    def __init__(self, mission_dict, l10n):
        super().__init__(mission_dict, l10n)
        self.weather = Weather(self.d, l10n)
        self._blue_coa = Coalition(self.d, l10n, 'blue')
        self._red_coa = Coalition(self.d, l10n, 'red')
        self.ground_control = GroundControl(self.d, l10n)

    def __repr__(self):
        return 'Mission({})'.format(self.d)

    @property
    def theatre(self) -> str:
        """
        :return: mission theater
        :rtype: str
        """
        return self.d['theatre']

    @property
    def blue_coa(self) -> 'Coalition':
        """
        Returns: blue coalition
        """
        return self._blue_coa  # type: ignore

    @property
    def red_coa(self) -> 'Coalition':
        """
        Returns: red coalitions
        """
        return self._red_coa  # type: ignore

    def farps(self) -> typing.Iterator['Static']:
        """
        Returns: generator over all FARPs objects
        """
        for coa in [self._blue_coa, self._red_coa]:
            if coa is not None:
                for farp in coa.farps:
                    yield farp


# noinspection PyProtectedMember
class Coalition(BaseMissionObject):
    """
    Represents a coalition
    """

    def __init__(self, mission_dict, ln10, coa_color):
        super().__init__(mission_dict, ln10)
        self.coa_color = coa_color
        self._countries = {}

    def __repr__(self):
        return 'Coalition({}, {})'.format(self._section_coalition, self.coa_color)

    def __eq__(self, other):
        if not isinstance(other, Coalition):
            raise ValueError('"other" must be an Coalition instance; got: {}'.format(type(other)))
        return self._section_coalition == other._section_coalition

    @property
    def _section_coalition(self):
        return self.d['coalition'][self.coa_color]

    @property
    def _section_bullseye(self):
        return self._section_coalition['bullseye']

    @property
    def bullseye_x(self) -> float:
        """
        Returns: bullseye X coordinate
        """
        return self._section_bullseye['x']

    @property
    def bullseye_y(self) -> float:
        """
        Returns: bullseye Y coordinate
        """
        return self._section_bullseye['y']

    @property
    def bullseye_position(self) -> typing.Tuple[float, float]:
        """
        Returns: bullseye position
        """
        return self.bullseye_x, self.bullseye_y

    @property
    def _section_nav_points(self):
        return self._section_coalition['nav_points']

    @property
    def coalition_name(self) -> str:
        """
        Returns: coalition name
        """
        return self._section_coalition['name']

    @property
    def _section_country(self):
        return self._section_coalition['country']

    @property
    def countries(self) -> typing.Iterator['Country']:
        """
        Returns: generator over all countries in this coalition
        """
        for k in self._section_country:
            if k not in self._countries.keys():
                country = Country(self.d, self.l10n, self.coa_color, k)
                self._countries[k] = country
                self._countries_by_id[country.country_id] = country
                self._countries_by_name[country.country_name] = country
            yield self._countries[k]

    def get_country_by_name(self, country_name) -> 'Country':
        """
        Gets a country in this coalition by its name

        Args:
            country_name: country name

        Returns: Country
        """
        VALID_STR.validate(country_name, 'get_country_by_name', exc=ValueError)
        if country_name not in self._countries_by_name.keys():
            for country in self.countries:

                if country.country_name == country_name:
                    return country
            raise ValueError(country_name)
        else:
            return self._countries_by_name[country_name]

    def get_country_by_id(self, country_id) -> 'Country':
        """
        Gets a country in this coalition by its ID

        Args:
            country_id: country Id

        Returns: Country
        """
        VALID_POSITIVE_INT.validate(country_id, 'get_country_by_id', exc=ValueError)
        if country_id not in self._countries_by_id.keys():
            for country in self.countries:

                if country.country_id == country_id:
                    return country
            raise ValueError(country_id)
        else:
            return self._countries_by_id[country_id]

    @property
    def groups(self) -> typing.Iterator['Group']:
        """
        Returns: generator over all groups in this coalition
        """
        for country in self.countries:

            for group in country.groups:

                yield group

    @property
    def statics(self) -> typing.Iterator['Static']:
        """
        Returns: generator over all statics in this coalition
        """
        for country in self.countries:

            for static in country.statics:

                yield static

    @property
    def farps(self) -> typing.Iterator['Static']:
        """
        Returns: generator over all FARPs in this coalition
        """
        for static in self.statics:

            if static.static_is_farp:
                yield static

    def get_groups_from_category(self, category) -> typing.Iterator['Group']:
        """
        Args:
            category: group category

        Returns: generator over all groups from a specific category in this coalition
        """
        Mission.validator_group_category.validate(category, 'get_groups_from_category')
        for group in self.groups:

            if group.group_category == category:
                yield group

    def get_units_from_category(self, category) -> typing.Iterator['BaseUnit']:
        """
        Args:
            category: unit category

        Returns: generator over all units of a specific category in this coalition
        """
        Mission.validator_group_category.validate(category, 'group category')
        for unit in self.units:

            if unit.group_category == category:
                yield unit

    def get_group_by_id(self, group_id) -> typing.Optional['Group']:
        """
        Args:
            group_id: group ID

        Returns: Group
        """
        VALID_POSITIVE_INT.validate(group_id, 'get_group_by_id')
        for group in self.groups:

            if group.group_id == group_id:
                return group

        return None


class Trig(BaseMissionObject):
    """
    Represents a Trigger
    """

    def __init__(self, mission_dict, l10n):
        super().__init__(mission_dict, l10n)

    @property
    def _section_trig(self):
        return self.d['trig']


class Result(BaseMissionObject):
    """
    Represents a Result
    """

    def __init__(self, mission_dict, l10n):
        super().__init__(mission_dict, l10n)

    @property
    def _section_result(self):
        return self.d['result']


class GroundControl(BaseMissionObject):
    """
    Represents GroundControl
    """
    validator_commander = Validator(_type=int, _min=0, _max=100, exc=ValueError, logger=LOGGER)

    def __init__(self, mission_dict, l10n):
        super().__init__(mission_dict, l10n)

    def __repr__(self):
        return 'GroundControl({})'.format(self._section_ground_control)

    @property
    def _section_ground_control(self):
        return self.d['groundControl']

    @property
    def _section_ground_control_roles(self):
        return self.d['groundControl']['roles']

    @property
    def pilots_control_vehicles(self):
        """
        Returns: whether or not pilots can control vehicles
        """
        return self._section_ground_control['isPilotControlVehicles']

    @pilots_control_vehicles.setter
    def pilots_control_vehicles(self, value):
        VALID_BOOL.validate(value, 'pilots_control_vehicles')
        self._section_ground_control['isPilotControlVehicles'] = value

    @property
    def _section_artillery_commander(self):
        return self._section_ground_control_roles['artillery_commander']

    @property
    def artillery_commander_red(self) -> int:
        """
        Returns: amount of artillery commander in red coa
        """
        return self._section_artillery_commander['red']

    @artillery_commander_red.setter
    def artillery_commander_red(self, value):
        self.validator_commander.validate(value, 'artillery_commander_red')
        self._section_artillery_commander['red'] = value

    @property
    def instructor_blue(self) -> int:
        """
        Returns: amount in instructors in blue coa
        """
        return self._section_instructor['blue']

    @instructor_blue.setter
    def instructor_blue(self, value):
        self.validator_commander.validate(value, 'instructor_blue')
        self._section_instructor['blue'] = value

    @property
    def instructor_red(self) -> int:
        """
        Returns: amount of instructors in red coa
        """
        return self._section_instructor['red']

    @instructor_red.setter
    def instructor_red(self, value):
        self.validator_commander.validate(value, 'instructor_red')
        self._section_instructor['red'] = value

    @property
    def _section_observer(self):
        return self._section_ground_control_roles['observer']

    @property
    def observer_blue(self) -> int:
        """
        Returns: amount in observers in blue coa
        """
        return self._section_observer['blue']

    @observer_blue.setter
    def observer_blue(self, value):
        self.validator_commander.validate(value, 'observer_blue')
        self._section_observer['blue'] = value

    @property
    def observer_red(self) -> int:
        """
        Returns: amounts of observers in red coa
        """
        return self._section_observer['red']

    @observer_red.setter
    def observer_red(self, value):
        self.validator_commander.validate(value, 'observer_red')
        self._section_observer['red'] = value

    @property
    def _section_forward_observer(self):
        return self._section_ground_control_roles['forward_observer']

    @property
    def forward_observer_blue(self) -> int:
        """
        Returns: amount of FO in blue coa
        """
        return self._section_forward_observer['blue']

    @forward_observer_blue.setter
    def forward_observer_blue(self, value):
        self.validator_commander.validate(value, 'forward_observer_blue')
        self._section_forward_observer['blue'] = value

    @property
    def forward_observer_red(self) -> int:
        """
        Returns: amount of FO in red coa
        """
        return self._section_forward_observer['red']

    @forward_observer_red.setter
    def forward_observer_red(self, value):
        self.validator_commander.validate(value, 'forward_observer_red')
        self._section_forward_observer['red'] = value

    @property
    def artillery_commander_blue(self) -> int:
        """
        Returns: amount of arty commanders in blue coa
        """
        return self._section_artillery_commander['blue']

    @artillery_commander_blue.setter
    def artillery_commander_blue(self, value):
        self.validator_commander.validate(value, 'artillery_commander_blue')
        self._section_artillery_commander['blue'] = value

    @property
    def _section_instructor(self):
        return self._section_ground_control_roles['instructor']


# noinspection PyProtectedMember
class Weather(BaseMissionObject):
    """
    Represents the weather
    """
    validator_precipitations = Validator(_type=int, _min=0, _max=4, exc=ValueError, logger=LOGGER)
    validator_cloud_density = Validator(_type=int, _min=0, _max=10, exc=ValueError, logger=LOGGER)
    validator_cloud_thickness = Validator(_type=int, _min=200, _max=2000, exc=ValueError,
                                          logger=LOGGER)
    validator_cloud_base = Validator(_type=int, _min=300, _max=5000, exc=ValueError, logger=LOGGER)
    validator_fog_visibility = Validator(_type=int, _min=0, _max=6000, exc=ValueError,
                                         logger=LOGGER)
    validator_dust_density = Validator(_type=int, _min=300, _max=3000, exc=ValueError,
                                       logger=LOGGER)
    validator_visibility = Validator(_type=int, _min=0, _max=80000, exc=ValueError,
                                     logger=LOGGER)
    validator_fog_thickness = Validator(_type=int, _min=0, _max=1000, exc=ValueError,
                                        logger=LOGGER)
    validator_qnh = Validator(_type=int, _min=720, _max=790, exc=ValueError, logger=LOGGER)
    validator_temperature = Validator(_type=int, _min=-50, _max=50, exc=ValueError, logger=LOGGER)
    validator_temp_spring_or_fall = Validator(_type=int, _min=-10, _max=30, exc=ValueError,
                                              logger=LOGGER)
    validator_temp_winter = Validator(_type=int, _min=-50, _max=15, exc=ValueError, logger=LOGGER)
    validator_temp_summer = Validator(_type=int, _min=5, _max=50, exc=ValueError, logger=LOGGER)
    seasons_enum = {
        1: {
            'name': 'summer',
            'temp_validator': validator_temp_summer,
        },
        2: {
            'name': 'winter',
            'temp_validator': validator_temp_winter,
        },
        3: {
            'name': 'spring',
            'temp_validator': validator_temp_spring_or_fall,
        },
        4: {
            'name': 'fall',
            'temp_validator': validator_temp_spring_or_fall,
        },
        'summer': 1,
        'winter': 2,
        'spring': 3,
        'fall': 4,
    }
    validator_season_name = Validator(_type=str, _in_list=['summer', 'winter', 'fall', 'spring'],
                                      exc=ValueError, logger=LOGGER)
    validator_season_code = Validator(_type=int, _min=1, _max=4, exc=ValueError, logger=LOGGER)
    validator_turbulence = Validator(_type=int, _min=0, _max=60, exc=ValueError, logger=LOGGER)
    validator_atmo_type = Validator(_type=int, _min=0, _max=1, exc=ValueError, logger=LOGGER)
    validator_wind_speed = Validator(_type=int, _min=0, _max=50, exc=ValueError, logger=LOGGER)

    def __init__(self, mission_dict, l10n):
        super().__init__(mission_dict, l10n)

    def __repr__(self):
        return 'Weather({})'.format(self._section_weather)

    def __eq__(self, other):
        if not isinstance(other, Weather):
            raise ValueError('"other" must be an Weather instance; got: {}'.format(type(other)))
        return self._section_weather == other._section_weather

    def get_season_code_from_name(self, season_name) -> int:
        """
        Args:
            season_name: season name

        Returns: season code
        """
        self.validator_season_name.validate(season_name, 'get_season_code_from_name')
        return self.seasons_enum[season_name]  # type: ignore

    @property
    def _section_wind_at_ground_level(self):
        return self._section_wind['atGround']

    @property
    def turbulence(self) -> float:
        """
        Returns: turbulence at ground level
        """
        return self._section_weather['groundTurbulence']

    @turbulence.setter
    def turbulence(self, value):
        self.validator_turbulence.validate(value, 'turbulence')
        self._section_weather['groundTurbulence'] = value

    @property
    def wind_ground_speed(self) -> int:
        """
        Returns: winds at ground level in ms
        """
        return self._section_wind_at_ground_level['speed']

    @wind_ground_speed.setter
    def wind_ground_speed(self, value):
        self.validator_wind_speed.validate(value, 'wind_ground_speed')
        self._section_wind_at_ground_level['speed'] = value

    @property
    def _section_fog(self):
        return self._section_weather['fog']

    @property
    def fog_thickness(self) -> int:
        """
        Returns: fog thickness in meters
        """
        return self._section_fog['thickness']

    @fog_thickness.setter
    def fog_thickness(self, value):
        self.validator_fog_thickness.validate(value, 'fog_thickness')
        self._section_fog['thickness'] = value

    @property
    def fog_visibility(self) -> int:
        """
        Returns: fog visibility in meters
        """
        return self._section_fog['visibility']

    @fog_visibility.setter
    def fog_visibility(self, value):
        self.validator_fog_visibility.validate(value, 'fog_visibility')
        self._section_fog['visibility'] = value

    @property
    def fog_enabled(self) -> bool:
        """
        Returns: True if fog is enabled
        """
        return self._section_weather['enable_fog']

    @fog_enabled.setter
    def fog_enabled(self, value: bool):
        VALID_BOOL.validate(value, 'enable_fog')
        self._section_weather['enable_fog'] = value

    @property
    def dust_enabled(self) -> bool:
        """
        Returns: True if fog is enabled
        """
        try:
            return self._section_weather['enable_dust']
        except KeyError:
            return False

    @dust_enabled.setter
    def dust_enabled(self, value: bool):
        VALID_BOOL.validate(value, 'dust_enabled')
        self._section_weather['enable_dust'] = value

    @property
    def dust_density(self) -> int:
        """
        Returns: fog visibility in meters
        """
        try:
            return self._section_weather['dust_density']
        except KeyError:
            return 3000

    @dust_density.setter
    def dust_density(self, value: int):
        self.validator_dust_density.validate(value, 'dust_density')
        self._section_weather['dust_density'] = value

    @property
    def _section_visibility(self):
        return self._section_weather['visibility']

    @property
    def visibility(self) -> int:
        """
        Returns: visibility in meters
        """
        return self._section_visibility['distance']

    @visibility.setter
    def visibility(self, value):
        self.validator_visibility.validate(value, 'visibility')
        self._section_visibility['distance'] = value

    @property
    def precipitation_code(self) -> int:
        """
        Returns: precipitation code
        """
        return self._section_clouds['iprecptns']

    @precipitation_code.setter
    def precipitation_code(self, value):
        self.validator_precipitations.validate(value, 'precipitation_code')
        if value > 0 and self.cloud_density <= 4:
            raise ValueError('No rain or snow if cloud density is less than 5')
        if value in [2, 4] and self.cloud_density <= 8:
            raise ValueError('No thunderstorm or snowstorm if cloud density is less than 9')
        if value > 2 and self.temperature > 0:
            raise ValueError('No snow with temperature over 0; use rain or thunderstorm instead')
        if value in [1, 2] and self.temperature < 0:
            raise ValueError(
                'No rain or thunderstorm if temperature is below 0; use snow or snowstorm instead')
        self._section_clouds['iprecptns'] = value

    @property
    def wind_at8000_dir(self) -> int:
        """
        Returns: wind direction at 8000m
        """
        return self._section_wind_at8000['speed']

    @wind_at8000_dir.setter
    def wind_at8000_dir(self, value):
        Mission.validator_heading.validate(value, 'wind_at8000_dir')
        self._section_wind_at8000['dir'] = value

    @property
    def _section_weather(self):
        return self.d['weather']

    @property
    def temperature(self) -> int:
        """
        Returns: temperature in Celsius
        """
        return self._section_season['temperature']

    @temperature.setter
    def temperature(self, value):
        self.validator_temperature.validate(value, 'temperature')
        self._section_season['temperature'] = value
        # if value > 0 and self.precipitation_code > 2:
        #     self.precipitation_code -= 2
        # if value < 0 < self.precipitation_code < 3:  # PyKek
        #     self.precipitation_code += 2

    @property
    def _section_wind_at8000(self):
        return self._section_wind['at8000']

    @property
    def wind_ground_dir(self) -> int:
        """
        Returns: wind speed at ground level
        """
        return self._section_wind_at_ground_level['dir']

    @wind_ground_dir.setter
    def wind_ground_dir(self, value):
        Mission.validator_heading.validate(value, 'wind_ground_dir')
        self._section_wind_at_ground_level['dir'] = value

    @property
    def _section_wind(self):
        return self._section_weather['wind']

    @property
    def _section_wind_at2000(self):
        return self._section_wind['at2000']

    @property
    def season_name(self) -> str:
        """
        Returns: name of the season
        """
        return self.seasons_enum[self.season_code]['name']  # type: ignore

    @property
    def altimeter(self) -> int:
        """
        Returns: pressure in mmHg
        """
        return self._section_weather['qnh']

    @altimeter.setter
    def altimeter(self, value):
        self.validator_qnh.validate(value, 'altimeter')
        self._section_weather['qnh'] = value

    @property
    def wind_at2000_speed(self) -> int:
        """
        Returns: wind speed at 2000 meters
        """
        return self._section_wind_at2000['speed']

    @wind_at2000_speed.setter
    def wind_at2000_speed(self, value):
        self.validator_wind_speed.validate(value, 'wind_at2000_speed')
        self._section_wind_at2000['speed'] = value

    @property
    def wind_at2000_dir(self) -> int:
        """
        Returns: wind direction at 2000 meters
        """
        return self._section_wind_at2000['dir']

    @wind_at2000_dir.setter
    def wind_at2000_dir(self, value):
        Mission.validator_heading.validate(value, 'wind_at2000_dir')
        self._section_wind_at2000['dir'] = value

    @property
    def _section_season(self):
        return self._section_weather['season']

    @property
    def atmosphere_type(self) -> int:
        """
        Returns: atmosphere type (0: static, 1: dynamic)
        """
        return self._section_weather['atmosphere_type']

    @atmosphere_type.setter
    def atmosphere_type(self, value):
        self.validator_atmo_type.validate(value, 'atmosphere_type')
        self._section_weather['atmosphere_type'] = value

    @property
    def season_code(self) -> int:
        """
        Returns: season code
        """
        return self._section_season['iseason']

    @season_code.setter
    def season_code(self, value):
        self.validator_season_code.validate(value, 'season')
        self._section_season['iseason'] = value
        if self.temperature < self.seasons_enum[value]['temp_validator'].min:
            self.temperature = self.seasons_enum[value]['temp_validator'].min
        if self.temperature > self.seasons_enum[value]['temp_validator'].max:
            self.temperature = self.seasons_enum[value]['temp_validator'].max

    @property
    def _section_clouds(self):
        return self._section_weather['clouds']

    @property
    def cloud_thickness(self) -> int:
        """
        Returns: cloud thickness
        """
        return self._section_clouds['thickness']

    @cloud_thickness.setter
    def cloud_thickness(self, value):
        self.validator_cloud_thickness.validate(value, 'cloud_thickness')
        self._section_clouds['thickness'] = value

    @property
    def cloud_base(self) -> int:
        """
        Returns: cloud base
        """
        return self._section_clouds['base']

    @cloud_base.setter
    def cloud_base(self, value):
        self.validator_cloud_base.validate(value, 'cloud_base')
        self._section_clouds['base'] = value

    @property
    def cloud_density(self) -> int:
        """
        Returns: cloud density (0 to 10)
        """
        return self._section_clouds['density']

    @cloud_density.setter
    def cloud_density(self, value):
        self.validator_cloud_density.validate(value, 'cloud_density')
        self._section_clouds['density'] = value

    @property
    def wind_at8000_speed(self) -> int:
        """
        Returns: wind speed at 8000 meters
        """
        return self._section_wind_at8000['speed']

    @wind_at8000_speed.setter
    def wind_at8000_speed(self, value):
        self.validator_wind_speed.validate(value, 'wind_at8000_speed')
        self._section_wind_at8000['speed'] = value


# noinspection PyProtectedMember
class Country(Coalition):
    """
    Represents a Country
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index):
        super().__init__(mission_dict, l10n, coa_color)
        self.__groups = {
            'helicopter': {},
            'plane': {},
            'vehicle': {},
            'ship': {},
        }
        self.country_index = country_index
        self.__static = {}

    def __repr__(self):
        return 'Country({}, {}, {})'.format(self._section_country, self.coa_color, self.country_index)

    def __eq__(self, other):
        if not isinstance(other, Country):
            raise ValueError('"other" must be an Country instance; got: {}'.format(type(other)))
        return self._section_country == other._section_country

    @property
    def _section_this_country(self):
        return self._section_coalition['country'][self.country_index]

    @property
    def country_id(self) -> int:
        """
        Returns: country Id
        """
        return self._section_this_country['id']

    @property
    def country_name(self) -> str:
        """
        Returns: country name
        """
        return self._section_this_country['name']

    @property
    def groups(self) -> typing.Iterator['Group']:
        """
        Returns: generator of all groups in this country
        """
        for group_category in Mission.valid_group_categories:
            if group_category in self._section_this_country.keys():
                for group_index in self._section_this_country[group_category]['group']:
                    if group_index not in self.__groups[group_category]:
                        self.__groups[group_category][group_index] = Group(self.d, self.l10n, self.coa_color,
                                                                           self.country_index, group_category,
                                                                           group_index)
                    yield self.__groups[group_category][group_index]

    @property
    def statics(self) -> typing.Iterator['Static']:
        """
        Returns: generator of all statics in this country
        """
        if 'static' in self._section_this_country.keys():
            for static_index in self._section_this_country['static']['group']:
                if static_index not in self.__static:
                    self.__static[static_index] = Static(self.d, self.l10n, self.coa_color,
                                                         self.country_index, static_index)
                yield self.__static[static_index]

    def get_groups_from_category(self, category) -> typing.Iterator['Group']:
        """
        Args:
            category: category

        Returns: all groups from a specific category in this country
        """
        Mission.validator_group_category.validate(category, 'get_groups_from_category')
        for group in self.groups:

            if group.group_category == category:
                yield group

    def get_group_by_id(self, group_id) -> typing.Optional['Group']:
        """
        Args:
            group_id: group id

        Returns: Group
        """
        for group in self.groups:

            if group.group_id == group_id:
                return group

        return None


class Static(Country):
    """
    Represents a static
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index, static_index):
        super(Static, self).__init__(mission_dict, l10n, coa_color, country_index)
        self.static_index = static_index

    @property
    def static_id(self) -> int:
        """
        Returns: static id
        """
        return self._section_static['groupId']

    @static_id.setter
    def static_id(self, value):
        VALID_INT.validate(value, 'groupId')
        self._section_static['groupId'] = value

    @property
    def _section_static(self):
        return self._section_this_country['static']['group'][self.static_index]

    @property
    def _static_name_key(self):
        return self._section_static['name']

    @property
    def static_name(self) -> str:
        """
        Returns: static name
        """
        return self.l10n[self._static_name_key]

    @static_name.setter
    def static_name(self, value):
        validator_group_or_unit_name.validate(value, 'group name')
        self.l10n[self._static_name_key] = value

    @property
    def static_category(self) -> str:
        """
        Returns: static category
        """
        return self._section_static['units'][1]['category']

    @property
    def static_is_farp(self) -> bool:
        """
        Returns: True if statics is a Farp
        """
        return self.static_category == 'Heliports'

    @property
    def static_position(self) -> typing.Tuple[float, float]:
        """
        Returns: position of this static
        """
        unit = self._section_static['units'][1]
        return unit['x'], unit['y']


# noinspection PyProtectedMember
class Group(Country):
    """
    Represents a Group
    """
    attribs = ('group_category', 'group_index', 'group_hidden', 'group_start_time', '_group_name_key')

    class Route:
        """
        Represents a set of waypoints
        """

        class Point:
            """
            Represents a waypoint
            """

            def __init__(self, parent_route):
                self.parent_route = parent_route

            def __repr__(self):
                return 'Route({})'.format(self.parent_route.parent_group.group_name)

        def __init__(self, parent_group):
            self.parent_group = parent_group

        def __repr__(self):
            return 'Route({})'.format(self.parent_group.group_name)

        @property
        def _section_route(self):
            return self.parent_group._section_group['route']['points']

        @property
        def points(self):
            """
            Returns: list of waypoints in this route
            """
            raise NotImplementedError('uh')

    validator_group_route = Validator(_type=Route, exc=ValueError, logger=LOGGER)
    units_class_enum = None

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index):
        super().__init__(mission_dict, l10n, coa_color, country_index)
        self.group_category = group_category
        self.group_index = group_index
        self.__group_route = None
        self.__units = {}
        self.units_class_enum = {
            'helicopter': Helicopter,
            'plane': Plane,
            'ship': Ship,
            'vehicle': Vehicle,
        }

    def __repr__(self):
        return 'Group({}, {}, {}, {}, {})'.format(self._section_group, self.coa_color, self.country_index,
                                                  self.group_category, self.group_index)

    def __eq__(self, other):
        if not isinstance(other, Group):
            raise ValueError(
                '"other" must be an AbstractUnit instance; got: {}'.format(type(other)))
        return self._section_group == other._section_group

    # noinspection PyTypeChecker
    @property
    def group_route(self) -> 'Group.Route':
        """
        Returns: route of this group
        """
        #  TODO
        if self.__group_route is None:
            self.__group_route = Group.Route(self)
        return self.__group_route

    @group_route.setter
    def group_route(self, value):
        self.validator_group_route.validate(value, 'group_route')
        self.__group_route = value

    @property
    def _section_group(self):
        return self._section_this_country[self.group_category]['group'][self.group_index]

    @property
    def _group_name_key(self):
        return self._section_group['name']

    @property
    def group_name(self) -> str:
        """
        Returns: group name
        """
        return self.l10n[self._group_name_key]

    @group_name.setter
    def group_name(self, value):
        validator_group_or_unit_name.validate(value, 'group name')
        self.l10n[self._group_name_key] = value

    @property
    def group_hidden(self) -> bool:
        """
        Returns: true if this group is hidden
        """
        return self._section_group['hidden']

    @group_hidden.setter
    def group_hidden(self, value):
        VALID_BOOL.validate(value, 'property "hidden" for group')
        self._section_group['hidden'] = value

    @property
    def group_id(self) -> int:
        """
        Returns: group id
        """
        return self._section_group['groupId']

    @group_id.setter
    def group_id(self, value):
        VALID_INT.validate(value, 'groupId')
        self._section_group['groupId'] = value

    @property
    def group_start_delay(self) -> int:
        """
        Returns: group start delay
        """
        return self._section_group['start_time']

    @group_start_delay.setter
    def group_start_delay(self, value):
        VALID_INT.validate(value, 'group_start_delay')
        if value < 0:
            raise ValueError(self.group_name)
        self._section_group['start_time'] = value

    @property
    def group_start_time(self) -> int:
        """
        Returns: group actual start time
        """
        return self.group_start_delay + self.mission_start_time

    @group_start_time.setter
    def group_start_time(self, value):
        VALID_INT.validate(value, 'group_start_time')
        self.group_start_delay = value - self.mission_start_time

    @property
    def group_start_date_time_as_string(self) -> str:
        """
        Returns: group start time as a string
        """
        return self._start_datetime_as_string(self.group_start_time)

    @property
    def units(self) -> typing.Iterator['BaseUnit']:
        """
        Returns: generator over all units of this group
        """
        for unit_index in self._section_group['units']:
            if unit_index not in self.__units.keys():
                _category = self.units_class_enum[self.group_category]  # type: ignore
                self.__units[unit_index] = _category(self.d, self.l10n, self.coa_color,
                                                     self.country_index,
                                                     self.group_category,
                                                     self.group_index, unit_index)
            yield self.__units[unit_index]

    @property
    def first_unit(self) -> 'BaseUnit':
        """
        Returns: gris unit of this group
        """
        return list(self.units)[0]

    def group_size(self) -> int:
        """
        Returns: amount of units in this group
        """
        return len(list(self.units))

    def get_unit_by_index(self, unit_index) -> typing.Optional['BaseUnit']:
        """
        Args:
            unit_index: index of unit

        Returns: a unit of this group
        """
        if unit_index in self._section_group['units'].keys():
            if unit_index not in self.__units.keys():
                _category = self.units_class_enum[self.group_category]  # type: ignore
                self.__units[unit_index] = _category(self.d, self.l10n, self.coa_color,
                                                     self.country_index,
                                                     self.group_category,
                                                     self.group_index, unit_index)
            return self.__units[unit_index]
        return None

    @property
    def group_is_client_group(self) -> bool:
        """
        Returns: True if this group is a client group
        """
        # TODO create test
        first_unit = self.get_unit_by_index(1)
        if first_unit:
            return first_unit.skill == 'Client'

        return False

    @property
    def group_start_position(self) -> typing.Tuple[float, float]:
        """
        Returns: group position
        """
        return self.group_route._section_route[1]['action']


# noinspection PyProtectedMember
class BaseUnit(Group):
    """
    Represents a Unit
    """
    validator_skill = Validator(_type=str,
                                _in_list=['Average', 'Good', 'High', 'Excellent', 'Random', 'Client', 'Player'],
                                exc=ValueError, logger=LOGGER)
    validator_unit_types = Validator(_type=str, _in_list=[], exc=ValueError, logger=LOGGER)

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index)
        self.unit_index = unit_index

    def __repr__(self):
        return '{}({}, {}, {}, {}, {}, {})'.format(self.__class__.__name__, self._section_unit, self.coa_color,
                                                   self.country_index, self.group_category, self.group_index,
                                                   self.unit_index)

    @property
    def _section_unit(self):
        return self._section_group['units'][self.unit_index]

    @property
    def _unit_name_key(self):
        return self._section_unit['name']

    @property
    def unit_name(self) -> str:
        """
        Returns: unit name
        """
        return self.l10n[self._unit_name_key]

    @unit_name.setter
    def unit_name(self, value):
        validator_group_or_unit_name.validate(value, 'unit name')
        self.l10n[self._unit_name_key] = value

    @property
    def skill(self) -> str:
        """
        Returns: unit skill (one of 'Average', 'Good', 'High', 'Excellent', 'Random', 'Client', 'Player')
        """
        return self._section_unit['skill']

    @skill.setter
    def skill(self, value):
        self.validator_skill.validate(value, 'unit skill')
        self._section_unit['skill'] = value

    @property
    def speed(self) -> float:
        """
        Returns: unit speed
        """
        return self._section_unit['speed']

    @speed.setter
    def speed(self, value):
        VALID_FLOAT.validate(value, 'unit speed')
        self._section_unit['speed'] = value

    @property
    def unit_type(self) -> str:
        """
        Returns: unit type
        """
        return self._section_unit['type']

    @unit_type.setter
    def unit_type(self, value):
        self.validator_unit_types.validate(value, 'unit type')
        self._section_unit['type'] = value

    @property
    def unit_id(self) -> int:
        """
        Returns: unit type
        """
        return self._section_unit['unitId']

    @unit_id.setter
    def unit_id(self, value):
        VALID_INT.validate(value, 'unitId')
        self._section_unit['unitId'] = value

    @property
    def unit_pos_x(self) -> float:
        """
        Returns: unit x coordinate
        """
        return float(self._section_unit['x'])

    @unit_pos_x.setter
    def unit_pos_x(self, value):
        VALID_FLOAT.validate(value, 'unit position X coordinate')
        self._section_unit['x'] = value

    @property
    def unit_pos_y(self) -> float:
        """
        Returns: unit Y coordinate
        """
        return float(self._section_unit['y'])

    @unit_pos_y.setter
    def unit_pos_y(self, value):
        VALID_FLOAT.validate(value, 'unit position Y coordinate')
        self._section_unit['y'] = value

    @property
    def unit_position(self) -> typing.Tuple[float, float]:
        """
        Returns: unit position
        """
        return self.unit_pos_x, self.unit_pos_y

    @unit_position.setter
    def unit_position(self, value):
        self.unit_pos_x, self.unit_pos_y = value

    @property
    def heading(self) -> float:
        """
        Returns: unit heading
        """
        return self._section_unit['heading']

    @heading.setter
    def heading(self, value):
        Mission.validator_heading.validate(value, 'unit heading')
        self._section_unit['heading'] = value

    @property
    def radio_presets(self) -> typing.Iterator['FlyingUnit.RadioPresets']:
        """
        Returns: generator over unit radio presets
        """
        raise TypeError('unit #{}: {}'.format(self.unit_id, self.unit_name))

    @property
    def has_radio_presets(self) -> bool:
        """
        Returns: true if unit has radio presets
        """
        return all([self.skill == 'Client', self.unit_type in FlyingUnit.RadioPresets.radio_enum.keys()])

    def __eq__(self, other):
        if not isinstance(other, BaseUnit):
            raise ValueError(
                '"other" must be an AbstractUnit instance; got: {}'.format(type(other)))
        return self._section_unit == other._section_unit


class FlyingUnit(BaseUnit):
    """
    Represents a flying unit
    """
    validator_board_number = Validator(_type=str, _regex=r'[0-9]{3}', exc=ValueError,
                                       logger=LOGGER)

    class RadioPresets:
        """
        Represent a set of radio presets
        """
        radio_enum = {
            'Ka-50': {
                1: {
                    'radio_name': 'R828',
                    'min': 20,
                    'max': 59.9,
                    'channels_qty': 10,
                },
                2: {
                    'radio_name': 'ARK22',
                    'min': 0.15,
                    'max': 1.75,
                    'channels_qty': 16,
                },
            },
            'Mi-8MT': {
                1: {
                    'radio_name': 'R863',
                    'min': 100,
                    'max': 399.9,
                    'channels_qty': 20,
                },
                2: {
                    'radio_name': 'R828',
                    'min': 20,
                    'max': 59.9,
                    'channels_qty': 10,
                },
            },
            'UH-1H': {
                1: {
                    'radio_name': 'ARC51',
                    'min': 225,
                    'max': 399.97,
                    'channels_qty': 20,
                },
            },
            'F-86F Sabre': {
                1: {
                    'radio_name': 'ARC-27',
                    'min': 225,
                    'max': 399.9,
                    'channels_qty': 18,
                },
            },
            'M-2000C': {
                1: {
                    'radio_name': 'UHF',
                    'min': 225,
                    'max': 400,
                    'channels_qty': 20,
                },
                2: {
                    'radio_name': 'V/UHF',
                    'min': 118,
                    'max': 400,
                    'channels_qty': 20,
                },
            },
            'MiG-21Bis': {
                1: {
                    'radio_name': 'R-832',
                    'min': 80,
                    'max': 399.9,
                    'channels_qty': 20,
                },
            },
            'P-51D': {
                1: {
                    'radio_name': 'SCR552',
                    'min': 100,
                    'max': 156,
                    'channels_qty': 4,
                },
            },
            'TF-51D': {
                1: {
                    'radio_name': 'SCR552',
                    'min': 100,
                    'max': 156,
                    'channels_qty': 4,
                },
            },
            'SpitfireLFMkIX': {
                1: {
                    'radio_name': 'SCR522',
                    'min': 100,
                    'max': 156,
                    'channels_qty': 4,
                },
            },
            'Bf-109K-4': {
                1: {
                    'radio_name': 'FuG 16 ZY',
                    'min': 38,
                    'max': 156,
                    'channels_qty': 5,
                },
            },
            'FW-190D9': {
                1: {
                    'radio_name': 'FuG 16',
                    'min': 38.4,
                    'max': 42.4,
                    'channels_qty': 4,
                },
            },
            'SA342L': {
                1: {
                    'radio_name': 'FM Radio',
                    'min': 30,
                    'max': 87.975,
                    'channels_qty': 8,
                },
            },
            'SA342M': {
                1: {
                    'radio_name': 'FM Radio',
                    'min': 30,
                    'max': 87.975,
                    'channels_qty': 8,
                },
            },
            'SA342Mistral': {
                1: {
                    'radio_name': 'FM Radio',
                    'min': 30,
                    'max': 87.975,
                    'channels_qty': 8,
                },
            },
        }

        def __init__(self, parent_unit, radio_num):

            self.parent_unit = parent_unit
            self.radio_num = radio_num

        def __eq__(self, other):
            if not isinstance(other, FlyingUnit.RadioPresets):
                raise Exception('cannot compare RadioPreset instance with other object of type {}'.format(type(other)))

            if not self.radio_name == other.radio_name:
                return False
            for channel, frequency in self.channels:
                if not frequency == other.get_frequency(channel):
                    return False
            return True

        @property
        def radio_name(self) -> str:
            """
            Returns: name of the radio
            """
            return self.radio_enum[self.parent_unit.unit_type][self.radio_num]['radio_name']  # type: ignore

        @property
        def channels_qty(self) -> int:
            """
            Returns: amount of channels
            """
            return self.radio_enum[self.parent_unit.unit_type][self.radio_num]['channels_qty']  # type: ignore

        @property
        def min(self) -> float:
            """
            Returns: minimum frequency
            """
            return float(self.radio_enum[self.parent_unit.unit_type][self.radio_num]['min'])  # type: ignore

        @property
        def max(self) -> float:
            """
            Returns: maximum frequency
            """
            return float(self.radio_enum[self.parent_unit.unit_type][self.radio_num]['max'])  # type: ignore

        @property
        def _section_radio(self):
            return self.parent_unit._section_unit['Radio']

        @property
        def _section_channels(self):
            return self._section_radio[self.radio_num]['channels']

        @property
        def channels(self) -> typing.Iterator[tuple]:
            """
            Returns: a generator of tuple of channels and frequencies
            """
            for k in self._section_channels:
                yield (k, float(self._section_channels[k]))

        def get_frequency(self, channel: int) -> float:
            """
            Args:
                channel: channel

            Returns: frequency for this channel
            """
            VALID_POSITIVE_INT.validate(channel, 'get_frequency')
            if 1 <= channel <= self.channels_qty:
                return float(self._section_channels[channel])
            else:
                raise ValueError(
                    'channel {} for radio {} in aircraft {}'.format(channel, self.radio_name,
                                                                    self.parent_unit.unit_name))

        def set_frequency(self, channel: int, frequency: float):
            """
            Args:
                channel: channel
                frequency: frequency
            """
            VALID_POSITIVE_INT.validate(channel, 'set_frequency')
            VALID_FLOAT.validate(frequency, 'set_frequency')
            if 1 <= channel <= self.channels_qty:
                # noinspection PyTypeChecker
                if self.min <= frequency <= self.max:
                    self._section_channels[channel] = float(frequency)
                else:
                    raise ValueError(
                        'frequency {} for channel {} for radio {} in aircraft {}'.format(frequency, channel,
                                                                                         self.radio_name,
                                                                                         self.parent_unit.unit_name))
            else:
                raise ValueError(
                    'channel {} for radio {} in aircraft {}'.format(channel, self.radio_name,
                                                                    self.parent_unit.unit_name))

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index)

    @property
    def radio_presets(self) -> typing.Iterator['FlyingUnit.RadioPresets']:
        """
        Returns: radio presets for this unit
        """
        if self.skill == 'Client' and self.unit_type in FlyingUnit.RadioPresets.radio_enum.keys():
            for k in self._section_unit['Radio']:
                yield FlyingUnit.RadioPresets(self, k)
        else:
            raise TypeError('unit #{}: {}'.format(self.unit_id, self.unit_name))

    @property
    def radios(self) -> dict:
        """
        Returns: radio section of the dic
        """
        try:
            return self._section_unit['Radio']
        except KeyError:
            raise KeyError(self.unit_type)

    def get_radio_by_name(self, radio_name: str) -> 'RadioPresets':
        """
        Args:
            radio_name: radio name

        Returns: radio presets for this radio
        """
        if self.has_radio_presets:
            for k in FlyingUnit.RadioPresets.radio_enum[self.unit_type].keys():
                if radio_name == FlyingUnit.RadioPresets.radio_enum[self.unit_type][k]['radio_name']:
                    return FlyingUnit.RadioPresets(self, k)
            raise TypeError('{} for aircraft: {}'.format(radio_name, self.unit_type))
        else:
            raise TypeError('unit #{}: {}'.format(self.unit_id, self.unit_name))

    def get_radio_by_number(self, radio_number) -> 'RadioPresets':
        """
        Args:
            radio_number: radio number

        Returns: presets for this radio
        """
        if self.has_radio_presets:
            if radio_number in FlyingUnit.RadioPresets.radio_enum[self.unit_type].keys():
                return FlyingUnit.RadioPresets(self, radio_number)
            else:
                raise TypeError(
                    'radio number {} for aircraft: {}'.format(radio_number, self.unit_type))
        else:
            raise TypeError('unit #{}: {}'.format(self.unit_id, self.unit_name))

    @property
    def livery(self) -> str:
        """
        Returns: livery for this group
        """
        return self._section_unit['livery_id']

    @livery.setter
    def livery(self, value):
        # TODO validate livery_id
        VALID_STR.validate(value, 'unit livery')
        self._section_unit['livery_id'] = value

    @property
    def onboard_num(self) -> str:
        """
        Returns: onboard number for this group
        """
        return self._section_unit['onboard_num']

    @onboard_num.setter
    def onboard_num(self, value):
        FlyingUnit.validator_board_number.validate(value, 'unit onboard number')
        self._section_unit['onboard_num'] = value


class Helicopter(FlyingUnit):
    """
    Represents a Helicopter
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index)


class Plane(FlyingUnit):
    """
    Represents a Plane
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index)


class Vehicle(BaseUnit):
    """
    Represents a Vehicle
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index)


class Ship(BaseUnit):
    """
    Represents a Ship
    """

    def __init__(self, mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index):
        super().__init__(mission_dict, l10n, coa_color, country_index, group_category, group_index, unit_index)
