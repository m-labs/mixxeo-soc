from targets.mlabs_video import MiniSoC, get_vga_dvi, add_vga_tig

from mixxeolib import mixframebuffer, dvisampler

class VideomixerSoC(MiniSoC):
	csr_map = {
		"fb":					11,
		"dvisampler0":			12,
		"dvisampler0_edid_mem":	13,
		"dvisampler1":			14,
		"dvisampler1_edid_mem":	15,
	}
	csr_map.update(MiniSoC.csr_map)

	interrupt_map = {
		"dvisampler0":	3,
		"dvisampler1":	4,
	}
	interrupt_map.update(MiniSoC.interrupt_map)

	def __init__(self, platform, **kwargs):
		MiniSoC.__init__(self, platform, **kwargs)
		pads_vga, pads_dvi = get_vga_dvi(platform)
		self.submodules.fb = mixframebuffer.MixFramebuffer(pads_vga, pads_dvi,
			self.lasmixbar.get_master(), self.lasmixbar.get_master())
		add_vga_tig(platform, self.fb)
		self.submodules.dvisampler0 = dvisampler.DVISampler(platform.request("dvi_in", 2), self.lasmixbar.get_master())
		self.submodules.dvisampler1 = dvisampler.DVISampler(platform.request("dvi_in", 3), self.lasmixbar.get_master())

default_subtarget = VideomixerSoC
