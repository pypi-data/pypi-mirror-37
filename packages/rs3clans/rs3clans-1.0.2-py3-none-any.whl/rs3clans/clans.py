# Standard Imports
import csv

# Non-standard Imports
import requests


class ClanNotFoundError(Exception):
    """
    Error exception to be called when a clan is not found when trying to read the clan's URL using Rs3's Official API.

    Correct error handling when reading a clan::
        >>> import rs3clans
        >>> try:
        ...     clan_name = "oasdiuahsiubasiufbasuf"
        ...     clan = rs3clans.Clan(name=clan_name)
        ... except rs3clans.ClanNotFoundError:
        ...     print("Exception encountered!")
        Exception encountered!
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Clan:
    """Class with attributes of a Runescape Clan using Jagex's RS3 API

    Most of Runescape 3's API can be accessed at: http://runescape.wikia.com/wiki/Application_programming_interface

    ...

    Parameters
    ----------
    name : str
        The name of the clan. Does not need to be case-sensitive.
    set_exp : bool, optional
        If True, set.exp will be set with the total Exp from the clan. False by default.
    set_dict : bool, optional
        If True, self.member will be set with info from all members from the clan in dict format. True by default.

    Attributes
    ----------
    name : str
        The name of the clan. Set when creating object.
    exp : int or None
        The total Exp of the clan, or None if argument set_exp is False (False by default).
    member : dict or None
        All info from members in the clan in dictionary format as below::
            >>> member_info = {
            ...     'player_1': {
            ...         'exp': 225231234,
            ...         'rank': 'Leader'
            ...     },
            ...     'player_2': {
            ...     'exp': 293123082,
            ...     'rank': 'Overseer'
            ...    },
            ... }
        or None if argument set_dict is False (True by default).
    count : int
        The number of members in the Clan.
    avg_exp : int or None
         The average clan exp per member in the Clan, or None if either set_exp or set_dict arguments are False.

    Raises
    ------
    ClanNotFoundError
        If an invalid clan name is passed when creating object Clan.
    """

    def __init__(self, name, set_exp=False, set_dict=True):
        self.name = name
        self.exp = None
        self.member = None
        self.count = None
        self.avg_exp = None

        if set_exp is True:
            self.exp = self._list_sum()
        if set_dict is True:
            self.member = self.dict_lookup()
            self.count = len(self.member)
        if set_exp is True and set_dict is True:
            self.avg_exp = self.exp / self.count

    def list_lookup(self):
        """

        Used for getting all information available from a clan using Rs3's Clan API.
        Mainly used for calculating the total exp of a clan manually.

        Returns
        -------
        list
            All players information from a clan in list format like so::
                >>> clan_list = [
                ... ['Clanmate', ' Clan Rank', ' Total XP', ' Kills'],
                ... ['Pedim', 'Owner', '739711654', '2'],
                ... ['Tusoroxo', 'Deputy Owner', '1132958333', '0'],
                ... ]
        """
        clan_url = f'http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName={self.name}'

        with requests.Session() as session:
            download = session.get(clan_url)
            decoded = download.content.decode('windows-1252')
            clan_list = list(csv.reader(decoded.splitlines(), delimiter=','))
            if clan_list[0][0] != "Clanmate":
                raise ClanNotFoundError(f"Couldn't find clan: {self.name}")
            for row in clan_list:
                row[0] = row[0].replace(r"\xa0", " ")
            return clan_list

    def dict_lookup(self, rank_key="rank", exp_key="exp"):
        """

        Used for getting all information available from a clan using Rs3's Clan API.

        Contrary to `list_lookup` it returns it as a Dictionary format instead.
        The dict format makes easier to find info specific to certain members of the Clan instead of looping over it.

        Parameters
        ----------
        rank_key : str
            The key for Clan Rank to be used in the returned dictionary with all members info of clan.
        exp_key : str
            The key for Clan Exp to be used in the returned dictionary with all members info of clan.

        Returns
        --------
        dict
            Information from all members in the clan in dictionary format for ease of access.
        """
        clan_list = self.list_lookup()
        clan_dict = {}
        for row in clan_list[1:]:
            user_rank = row[1]
            username = row[0].replace('\xa0', ' ')
            user_exp = int(row[2])

            clan_dict[username] = {
                rank_key: user_rank,
                exp_key: user_exp
            }
        return clan_dict

    def get_member(self, name):
        """

        Used for searching information about a clan member by passing in its name case insensitively.

        Parameters
        ----------
        name : str
            The name of the player to be searched in clan.

        Returns
        --------
        dict
            Information of the member passed in, with the keys ['exp'] and ['rank'] (or any custom keys you might have
            passed when creating Clan object.
        """
        for key, value in self.member.items():
            if key.lower() == name.lower():
                return value

    def _list_sum(self):
        """
        Gets a clan list from `list_lookup` and sums the total exp of the clan.

        Returns
        -------
        int
            The total Exp of the Clan.
        """
        clan_list = self.list_lookup()
        return sum(int(row[2]) for row in clan_list[1:])

    def _dict_sum(self):
        """
        Gets a clan dictionary from :func: `dict_lookup` and sums the total exp of the clan.

        .. deprecated:: 0.4.0
            Use `list_sum` as it's much faster.

        Returns
        -------
        int
            The total Exp of the Clan.
        """
        clan_dict = self.dict_lookup()
        return sum(members['exp'] for members in clan_dict.values())

    def __str__(self):
        return f"Name: {self.name} Exp: {self.exp} Avg. Exp: {self.avg_exp} Number of Members: {self.count}"


if __name__ == '__main__':
    # Create Clan with the name "Atlantis"
    clan = Clan(name="Atlantis", set_exp=True)

    # Info from member "NRiver" (case-sensitive)
    print(clan.member['NRiver'])

    # Total Exp of the clan
    print(clan.exp)

    # Average Clan Exp per Member of the clan
    print(clan.avg_exp)

    # Clan Name as passed when creating object Clan
    print(clan.name)

    # Number of members in clan
    print(clan.count)

    clan_two = Clan("okafbjhvfjsdhbsdhfhbqjfbqwf")
    print(clan.name)
