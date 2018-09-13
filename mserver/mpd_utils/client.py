from mpd.base import mpd_commands, MPDClient, mpd_command_provider


@mpd_command_provider
class MServerMPDClient(MPDClient):
    @mpd_commands('insert')
    def nop(self, lines):
        pass
