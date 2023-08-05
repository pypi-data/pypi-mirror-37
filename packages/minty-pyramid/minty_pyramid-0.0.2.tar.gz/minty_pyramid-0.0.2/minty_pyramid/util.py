import re


class INIParser:
    def parse_array(self, setting: str) -> list:
        """Return a proper list from given ini setting.

        :param setting: The setting to parse, e.g.: minty_service.enable
        :type setting: str
        :return: A list of entries from the given ini setting
        :rtype: list
        """
        entries = re.split(r"(?:\n|,| )", setting)

        return [entry for entry in entries if entry]

    def parse_from_prefix(self, settings: dict, prefix: str) -> dict:
        """Combine a set of ini settings to a dict by a given prefix.

        Will return a dict like:

        "

            {
                "first": "1",
                "two": "two",
            }

        from settings like:

        "

            {
                "setting.group.first": "1",
                "setting.group.two": "two",
                "setting.othergroup.three": 3,
            }

        :param settings: A dict of settings
        :type settings: dict
        :param prefix: A prefix to combine
        :type prefix: str
        :return: A dict containing only the settings from given prefix
        :rtype: dict
        """
        group_settings = {
            key.replace(prefix + ".", ""): settings[key]
            for key in settings.keys()
            if key.startswith(prefix)
        }

        return group_settings
