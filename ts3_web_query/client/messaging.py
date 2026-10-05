
from .http_client import HttpClient
from ..constants import TargetMode
from ..types import Message, MessageContent, Complaint, BanEntry


class Messaging:
    """Text and offline messages, complaints and bans."""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def _list(self, command: str, model, params=None):
        response = await self.http_client.request_list(command, params=params)
        return [model.from_dict(item) for item in response]

    async def _banids(self, command: str, params=None, json_body=None) -> list[int]:
        response = await self.http_client.request(command, params=params, json_body=json_body)
        return [int(item['banid']) for item in response]

    # --- text messages -------------------------------------------------------------------

    async def send_text_message(self, targetmode: int, msg: str, target: int = 1) -> None:
        """
        Sends a text message.

        :param targetmode: See TargetMode: CLIENT (private), CHANNEL (current channel) or SERVER.
        :param msg: The message text.
        :param target: The client ID for TargetMode.CLIENT; ignored for channel and server messages
            (the server still requires the parameter, so it defaults to 1).
        """
        await self.http_client.request(
            'sendtextmessage', params={'targetmode': targetmode, 'target': target, 'msg': msg})

    async def send_private_message(self, clid: int, msg: str) -> None:
        """Shortcut for send_text_message with TargetMode.CLIENT."""
        return await self.send_text_message(TargetMode.CLIENT, msg, target=clid)

    # --- offline messages ----------------------------------------------------------------

    async def message_list(self) -> list[Message]:
        """Lists the offline messages in your inbox. Returns an empty list if it is empty."""
        return await self._list('messagelist', Message)

    async def message_add(self, cluid: str, subject: str, message: str) -> None:
        """Sends an offline message to the client with the given unique identifier."""
        await self.http_client.request(
            'messageadd', params={'cluid': cluid, 'subject': subject, 'message': message})

    async def message_del(self, msgid: int) -> None:
        """Deletes an offline message from your inbox."""
        await self.http_client.request('messagedel', params={'msgid': msgid})

    async def message_get(self, msgid: int) -> MessageContent:
        """Returns an offline message. This does not mark it as read."""
        response = await self.http_client.request('messageget', params={'msgid': msgid})
        return MessageContent.from_dict(response[0])

    async def message_update_flag(self, msgid: int, read: bool = True) -> None:
        """Marks an offline message as read (or unread)."""
        await self.http_client.request(
            'messageupdateflag', params={'msgid': msgid, 'flag': 1 if read else 0})

    # --- complaints ----------------------------------------------------------------------

    async def complain_list(self, tcldbid: int | None = None) -> list[Complaint]:
        """
        Lists complaints on the virtual server, optionally only those about one client.
        Returns an empty list if there are none.
        """
        params = {'tcldbid': tcldbid} if tcldbid is not None else None
        return await self._list('complainlist', Complaint, params)

    async def complain_add(self, tcldbid: int, message: str) -> None:
        """Submits a complaint about the client with database ID tcldbid."""
        await self.http_client.request('complainadd', params={'tcldbid': tcldbid, 'message': message})

    async def complain_del_all(self, tcldbid: int) -> None:
        """Deletes all complaints about a client."""
        await self.http_client.request('complaindelall', params={'tcldbid': tcldbid})

    async def complain_del(self, tcldbid: int, fcldbid: int) -> None:
        """Deletes the complaint about tcldbid that was submitted by fcldbid."""
        await self.http_client.request('complaindel', params={'tcldbid': tcldbid, 'fcldbid': fcldbid})

    # --- bans ----------------------------------------------------------------------------

    async def ban_client(
            self,
            clids: list[int],
            time: int | None = None,
            banreason: str | None = None
    ) -> list[int]:
        """
        Bans one or more online clients. Two ban rules (IP and unique ID) are created per client.

        :param clids: IDs of the clients to ban.
        :param time: Ban duration in seconds; omitted means permanent.
        :param banreason: Optional reason.
        :return: The IDs of the created ban rules.
        """
        body: dict = {'clid': list(clids)}
        if time is not None:
            body['time'] = time
        if banreason is not None:
            body['banreason'] = banreason
        return await self._banids('banclient', json_body=body)

    async def ban_list(self) -> list[BanEntry]:
        """Lists the active ban rules. Returns an empty list if there are none."""
        return await self._list('banlist', BanEntry)

    async def ban_add(
            self,
            ip: str | None = None,
            name: str | None = None,
            uid: str | None = None,
            time: int | None = None,
            banreason: str | None = None
    ) -> int:
        """
        Adds a ban rule. At least one of ip, name or uid must be given (ip and name are regexps).

        :param time: Ban duration in seconds; omitted means permanent.
        :return: The ID of the new ban rule.
        """
        params = {k: v for k, v in
                  {'ip': ip, 'name': name, 'uid': uid, 'time': time, 'banreason': banreason}.items()
                  if v is not None}
        if not any(k in params for k in ('ip', 'name', 'uid')):
            raise ValueError('At least one of ip, name or uid is required.')
        return (await self._banids('banadd', params=params))[0]

    async def ban_del(self, banid: int) -> None:
        """Deletes a ban rule."""
        await self.http_client.request('bandel', params={'banid': banid})

    async def ban_del_all(self) -> None:
        """Deletes ALL active ban rules on the virtual server."""
        await self.http_client.request('bandelall')
