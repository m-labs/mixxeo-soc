from targets.mlabs_video import MiniSoC, get_vga_dvi, add_vga_tig

from misoclib.mem.sdram.core.lasmicon import LASMIconSettings
from misoclib.video import dvisampler
from mixxeolib import mixframebuffer


class VideomixerSoC(MiniSoC):
    csr_map = {
        "fb":                   18,
        "dvisampler0":          19,
        "dvisampler0_edid_mem": 20,
        "dvisampler1":          21,
        "dvisampler1_edid_mem": 22,
    }
    csr_map.update(MiniSoC.csr_map)

    interrupt_map = {
        "dvisampler0": 3,
        "dvisampler1": 4,
    }
    interrupt_map.update(MiniSoC.interrupt_map)

    def __init__(self, platform, **kwargs):
        MiniSoC.__init__(self, platform,
            sdram_controller_settings=LASMIconSettings(with_bandwidth=True),
            **kwargs)
        pads_vga, pads_dvi = get_vga_dvi(platform)
        self.submodules.fb = mixframebuffer.MixFramebuffer(pads_vga, pads_dvi,
            self.sdram.crossbar.get_master(), self.sdram.crossbar.get_master())
        add_vga_tig(platform, self.fb)
        self.submodules.dvisampler0 = dvisampler.DVISampler(platform.request("dvi_in", 2),
                                                            self.sdram.crossbar.get_master())
        self.submodules.dvisampler1 = dvisampler.DVISampler(platform.request("dvi_in", 3),
                                                            self.sdram.crossbar.get_master())

default_subtarget = VideomixerSoC
