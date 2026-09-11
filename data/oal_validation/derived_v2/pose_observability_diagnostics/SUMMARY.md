# OAL Pose-Observability Diagnostic

**Diagnostic only. No estimator or calibration parameters are modified.**

## Predeclared independent cues

- centroid x/y: fixture-relative image-position proxies
- in-plane tilt: 2-D orientation control
- case width: apparent scale/depth proxy
- normalized body-width gradient and mouth/base width ratio: perspective/taper proxies
- end-face skew difference: projected end-face geometry proxy
- end-face sharpness log-ratio: depth/focus asymmetry proxy

## Correlations with within-specimen centered frozen-hybrid OAL

| Group | Cue | n | Pearson r | Spearman rho |
|---|---|---:|---:|---:|
| final_fixture2_development | centroid_x_px | 12 | +0.1542 | +0.1329 |
| final_fixture2_development | centroid_y_px | 12 | +0.9104 | +0.7343 |
| final_fixture2_development | in_plane_tilt_deg | 12 | +0.1745 | +0.2098 |
| final_fixture2_development | case_width_px | 12 | +0.4001 | +0.3706 |
| final_fixture2_development | body_width_gradient_norm | 12 | +0.1071 | -0.3077 |
| final_fixture2_development | body_width_ratio_mouth_to_base | 12 | +0.4448 | +0.0979 |
| final_fixture2_development | endface_skew_difference | 12 | -0.7984 | -0.6993 |
| final_fixture2_development | endface_sharpness_log_ratio | 12 | +0.3564 | +0.3357 |
| controlled_repositioning_121 | centroid_x_px | 10 | -0.0078 | -0.3091 |
| controlled_repositioning_121 | centroid_y_px | 10 | +0.7999 | +0.8424 |
| controlled_repositioning_121 | in_plane_tilt_deg | 10 | -0.7592 | -0.6606 |
| controlled_repositioning_121 | case_width_px | 10 | -0.2311 | -0.4061 |
| controlled_repositioning_121 | body_width_gradient_norm | 10 | -0.5985 | -0.7576 |
| controlled_repositioning_121 | body_width_ratio_mouth_to_base | 10 | -0.5482 | -0.3818 |
| controlled_repositioning_121 | endface_skew_difference | 10 | -0.1755 | -0.2727 |
| controlled_repositioning_121 | endface_sharpness_log_ratio | 10 | +0.5578 | +0.3818 |
| formal_v2_diagnostic | centroid_x_px | 180 | +0.0231 | +0.0211 |
| formal_v2_diagnostic | centroid_y_px | 180 | +0.0925 | +0.1057 |
| formal_v2_diagnostic | in_plane_tilt_deg | 180 | -0.1239 | -0.1671 |
| formal_v2_diagnostic | case_width_px | 180 | +0.0427 | +0.0495 |
| formal_v2_diagnostic | body_width_gradient_norm | 180 | -0.1590 | -0.1538 |
| formal_v2_diagnostic | body_width_ratio_mouth_to_base | 180 | -0.0985 | -0.1206 |
| formal_v2_diagnostic | endface_skew_difference | 180 | -0.0607 | -0.0628 |
| formal_v2_diagnostic | endface_sharpness_log_ratio | 180 | -0.1186 | -0.0945 |

## Fixed-position specimen 146 noise control

- hybrid_oal_in range: 0.000115151
- centroid_x_px range: 0.022325850
- centroid_y_px range: 0.123546062
- in_plane_tilt_deg range: 0.011932205
- case_width_px range: 0.020502093
- body_width_gradient_norm range: 0.002401678
- body_width_ratio_mouth_to_base range: 0.011588106
- endface_skew_difference range: 0.006635454
- endface_sharpness_log_ratio range: 0.032494983

## Guardrail

A cue is not a correction merely because it correlates retrospectively. A software pose-compensation path is credible only if a physically interpretable cue is visible in non-formal development data, exhibits the same relationship in the V2 mechanism check, and can be parameterized using non-formal data alone before any prospective V3 validation. Formal V2 must not be used to fit correction coefficients.
