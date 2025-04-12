from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from deebot_client.command import CommandResult
from deebot_client.commands.xml import GetBatteryInfo
from deebot_client.events import BatteryEvent
from deebot_client.message import HandlingState
from tests.commands import assert_command

from . import get_request_xml

if TYPE_CHECKING:
    from deebot_client.events.base import Event


@pytest.mark.parametrize(
    ("power", "expected_event"),
    [
        (40, BatteryEvent(40)),
    ],
    ids=["40_pct_battery"],
)
async def test_get_battery_info(power: int, expected_event: Event) -> None:
    json = get_request_xml(f"<ctl ret='ok'><battery power='{power}' /></ctl>")
    await assert_command(GetBatteryInfo(), json, expected_event)


@pytest.mark.parametrize(
    "xml",
    ["<ctl ret='error'/>", "<ctl ret='ok'></ctl>"],
    ids=["error", "no_state"],
)
async def test_get_battery_info_error(xml: str) -> None:
    json = get_request_xml(xml)
    await assert_command(
        GetBatteryInfo(),
        json,
        None,
        command_result=CommandResult(HandlingState.ANALYSE_LOGGED),
    )
