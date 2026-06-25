# Dependency Matrix

Abbreviations: `cfg` configure, `rdy` readiness prerequisite, `ast` assert state, `enb` enable state, `qlf` qualify/gate, `str` stream, `obs` observe, `drv` build-drive, `prd` produce.

| source \\ target | Control plane | Analog control | Timing subsystem | Frontend boundary | config_ready | timing_ready | alignment_ready | trigger_enable | spy_enable | Trigger pipeline | Spybuffer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Control plane |  | cfg | cfg |  |  |  |  |  |  |  |  |
| Analog control |  |  |  |  | ast |  |  |  |  |  |  |
| Timing subsystem |  |  |  |  |  | ast |  |  |  |  |  |
| Frontend boundary |  |  |  |  |  |  | ast |  |  |  |  |
| config_ready |  |  |  |  |  |  |  | enb | enb |  |  |
| timing_ready |  |  |  |  |  |  |  | enb | enb |  |  |
| alignment_ready |  |  |  |  |  |  |  | enb | enb |  |  |
| trigger_enable |  |  |  |  |  |  |  |  |  | qlf |  |
| spy_enable |  |  |  |  |  |  |  |  |  |  | qlf |
| Trigger pipeline |  |  |  |  |  |  |  |  |  |  |  |
| Spybuffer |  |  |  |  |  |  |  |  |  |  |  |
