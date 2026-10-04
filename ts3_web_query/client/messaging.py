from typing import Union

from .http_client import HttpClient
from ..constants import TargetMode
from ..utils import status_to_error
from ..types import TeamSpeakError, Message, MessageContent, Complaint, BanEntry


class Messaging:
    """Text and offline messages, complaints and bans."""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def _list(self, command: str, model, params=None):
        response = await self.http_client.request(command, params=params)
        if isinstance(response, list):
            return [model.from_dict(item) for item in response]
        if response is None:
            return []
        return TeamSpeakError(**response)

    async def _banids(self, command: str, params=None, json_body=None) -> Union[list[int], TeamSpeakError]:
        response = await self.http_client.request(command, params=params, json_body=json_body)
        if isinstance(response, list):
            return [int(item['banid']) for item in response]
        if response is None:
            return []
        return TeamSpeakError(**response)

    # --- text messages -------------------------------------------------------------------

    async def send_text_message(self, targetmode: int, msg: str, target: int = 1) -> TeamSpeakError:
        """
        Sends a text message.

        :param targetmode: See TargetMode: CLIENT (private), CHANNEL (current channel) or SERVER.
        :param msg: The message text.
        :param target: The client ID for TargetMode.CLIENT; ignored for channel and server messages
            (the server still requires the parameter, so it defaults to 1).
        """
        response = await self.http_client.request(
            'sendtextmessage', params={'targetmode': targetmode, 'target': target, 'msg': msg})
        return status_to_error(response)

    async def send_private_message(self, clid: int, msg: str) -> TeamSpeakError:
        """Shortcut for send_text_message with TargetMode.CLIENT."""
        return await self.send_text_message(TargetMode.CLIENT, msg, target=clid)

    # --- offline messages ----------------------------------------------------------------

    async def message_list(self) -> Union[list[Message], TeamSpeakError]:
        """Lists the offline messages in your inbox. Returns an error with code 1281 if it is empty."""
        return await self._list('messagelist', Message)

    async def message_add(self, cluid: str, subject: str, message: str) -> TeamSpeakError:
        """Sends an offline message to the client with the given unique identifier."""
        response = await self.http_client.request(
            'messageadd', params={'cluid': cluid, 'subject': subject, 'message': message})
        return status_to_error(response)

    async def message_del(self, msgid: int) -> TeamSpeakError:
        """Deletes an offline message from your inbox."""
        response = await self.http_client.request('messagedel', params={'msgid': msgid})
        return status_to_error(response)

    async def message_get(self, msgid: int) -> Union[MessageContent, TeamSpeakError]:
        """Returns an offline message. This does not mark it as read."""
        response = await self.http_client.request('messageget', params={'msgid': msgid})
        if isinstance(response, list):
            return MessageContent.from_dict(response[0])
        return TeamSpeakError(**response)

    async def message_update_flag(self, msgid: int, read: bool = True) -> TeamSpeakError:
        """Marks an offline message as read (or unread)."""
        response = await self.http_client.request(
            'messageupdateflag', params={'msgid': msgid, 'flag': 1 if read else 0})
        return status_to_error(response)

    # --- complaints ----------------------------------------------------------------------

    async def complain_list(self, tcldbid: int | None = None) -> Union[list[Complaint], TeamSpeakError]:
        """
        Lists complaints on the virtual server, optionally only those about one client.
        Returns an error with code 1281 if there are none.
        """
        params = {'tcldbid': tcldbid} if tcldbid is not None else None
        return await self._list('complainlist', Complaint, params)

    async def complain_add(self, tcldbid: int, message: str) -> TeamSpeakError:
        """Submits a complaint about the client with database ID tcldbid."""
        response = await self.http_client.request('complainadd', params={'tcldbid': tcldbid, 'message': message})
        return status_to_error(response)

    async def complain_del_all(self, tcldbid: int) -> TeamSpeakError:
        """Deletes all complaints about a client."""
        response = await self.http_client.request('complaindelall', params={'tcldbid': tcldbid})
        return status_to_error(response)

    async def complain_del(self, tcldbid: int, fcldbid: int) -> TeamSpeakError:
        """Deletes the complaint about tcldbid that was submitted by fcldbid."""
        response = await self.http_client.request('complaindel', params={'tcldbid': tcldbid, 'fcldbid': fcldbid})
        return status_to_error(response)

    # --- bans ----------------------------------------------------------------------------

    async def ban_client(
            self,
            clids: list[int],
            time: int | None = None,
            banreason: str | None = None
    ) -> Union[list[int], TeamSpeakError]:
        """
        Bans one or more online clients. Two ban rules (IP and unique ID) are created per client.

        :param clids: IDs of the clients to ban.
        :param time: Ban duration in seconds; omitted means permanent.
        :param banreason: Optional reason.
        :return: The IDs of the created ban rules or a TeamSpeakError.
        """
        body: dict = {'clid': list(clids)}
        if time is not None:
            body['time'] = time
        if banreason is not None:
            body['banreason'] = banreason
        return await self._banids('banclient', json_body=body)

    async def ban_list(self) -> Union[list[BanEntry], TeamSpeakError]:
        """Lists the active ban rules. Returns an error with code 1281 if there are none."""
        return await self._list('banlist', BanEntry)

    async def ban_add(
            self,
            ip: str | None = None,
            name: str | None = None,
            uid: str | None = None,
            time: int | None = None,
            banreason: str | None = None
    ) -> Union[int, TeamSpeakError]:
        """
        Adds a ban rule. At least one of ip, name or uid must be given (ip and name are regexps).

        :param time: Ban duration in seconds; omitted means permanent.
        :return: The ID of the new ban rule or a TeamSpeakError.
        """
        params = {k: v for k, v in
                  {'ip': ip, 'name': name, 'uid': uid, 'time': time, 'banreason': banreason}.items()
                  if v is not None}
        if not any(k in params for k in ('ip', 'name', 'uid')):
            raise ValueError('At least one of ip, name or uid is required.')
        result = await self._banids('banadd', params=params)
        return result[0] if isinstance(result, list) else result

    async def ban_del(self, banid: int) -> TeamSpeakError:
        """Deletes a ban rule."""
        response = await self.http_client.request('bandel', params={'banid': banid})
        return status_to_error(response)

    async def ban_del_all(self) -> TeamSpeakError:
        """Deletes ALL active ban rules on the virtual server."""
        response = await self.http_client.request('bandelall')
        return status_to_error(response)
