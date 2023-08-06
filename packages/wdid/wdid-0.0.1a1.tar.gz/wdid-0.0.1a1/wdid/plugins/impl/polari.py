import pathlib
import typing as typ
import xml.etree.ElementTree as ET
from datetime import date, datetime, time

from wdid.dt_util import AUCKLAND_TZ, UTC
from wdid.entrys import CombinedEntry, Entry
from wdid.fs_util import riterdir

polari_dir = pathlib.Path("~/.local/share/TpLogger/logs/").expanduser().resolve()


def parse_polari_chat_history(today: date) -> typ.Collection[Entry]:
    data: typ.List[Entry] = []
    for file in riterdir(polari_dir):
        if file.suffix == ".log":
            # .../<name>/<date>.log
            chatname = file.parts[-2]
            if chatname.lower() == "nickserv":
                continue
            room_data = []
            have_messaged = False
            try:
                root = ET.parse(str(file)).getroot()
            except ET.ParseError:
                continue
            for msgelm in root.iter("message"):
                time = datetime.strptime(msgelm.attrib["time"], "%Y%m%dT%H:%M:%S")
                time = (
                    time.replace(tzinfo=UTC)
                    .astimezone(AUCKLAND_TZ)
                    .replace(tzinfo=None)
                )
                if time.date() != today:
                    break
                msg = "".join(msgelm.itertext())
                sep = ":"
                if msgelm.attrib["type"] == "action":
                    sep = " "
                have_messaged = have_messaged or (
                    msgelm.attrib["name"] in ("opal", "opal_", "opal_nz")
                )
                msg = "{:<12}{:<3}{}".format(msgelm.attrib["name"], sep, msg)
                room_data.append(Entry(time, chatname, msg))
            if have_messaged:
                data += room_data
    return data
