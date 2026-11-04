# 논문 수집 대조 보고서 (pubs_reconciliation)

- 생성: 2026-11-03 21:16 · 스크립트 `scripts/fetch_publications.py`
- 결과: **표시 317편**, 숨김(needs_review/hidden) 1편, yaml 전체 318편, 제외 111건 (후보 DOI 428건)
- 네트워크 요청 0건(+ 무작위 재조회 10건), 캐시 사용 349건 (`.cache/pubs/`)

## 1. 완료 기준

| # | 기준 | 결과 |
|---|---|---|
| 1 | `validate.py --data-only` 오류 0 | 통과 (오류 0) |
| 2 | `pi.yaml` selected_dois 5편 표시 | 통과 |
| 3 | 표시 논문 수 250~450 | 통과 (317편) |
| 4 | 보고서 항목(출처별·교집합·제외·needs_review·단일 출처·연도별·불일치·재조회) | 아래 2~9절 |
| 5 | `build.py --theme basic && validate.py --theme basic` 오류 0 | 통과 (build rc 0, validate 오류 0) |

## 2. 출처별 개수

| 출처 | 원자료 | DOI 수 | 비고 |
|---|---|---|---|
| ORCID `0000-0003-2251-2579` | works 304건 (journal-article 270, preprint 34) | 302 | DOI 없는 항목 2건 |
| OpenAlex | works 554건 (article 437, conference-abstract 42, preprint 22, dataset 19, conference-paper 10, erratum 8, peer-review 6, supplementary-materials 4, review 3, other 2, software 1) | 402 | DOI 없는 항목 152건 |
| Crossref 저자 검색 | `J.-S. Kug` 전체 2920 중 2920건 조회, family=Kug 418건(이름 J.-S. 계열 405); `Jong-Seong Kug` 전체 412888 중 2000건 조회, family=Kug 368건(이름 J.-S. 계열 366) | 405 | 중복 제거 후. 성만 Kug인 다른 저자 논문 13건은 버림 |

OpenAlex author ID (이름 변형 검색 `Jong-Seong Kug`, `J.-S. Kug`, `Kug Jong-Seong`, `Kug` 결과 중 Kug + 이름 J로 시작, ORCID가 다르면 제외):

| ID | 이름 | works | ORCID | 소속 | 이 ID로 잡힌 works |
|---|---|---|---|---|---|
| A5091389074 | Jong‐Seong Kug | 554 | 0000-0003-2251-2579 | Seoul National University | 552 |
| A5034326367 | Kug Jong-Seong | 1 | - |  | 1 |
| A5069317737 | Kug J-S | 1 | - |  | 1 |

## 3. 출처 교집합

| 출처 조합 | 후보 DOI 전체 | 표시 | 숨김 |
|---|---|---|---|
| orcid ∩ openalex ∩ crossref | 288 | 260 | 0 |
| openalex ∩ crossref | 92 | 56 | 0 |
| orcid ∩ crossref | 13 | 0 | 0 |
| orcid ∩ openalex | 0 | 1 | 0 |
| crossref 만 | 12 | 0 | 1 |
| openalex 만 | 22 | 0 | 0 |
| 합계 | 427 | 317 | 1 |

(후보 DOI 전체 열은 ORCID 오기로 정정돼 출처가 비게 된 DOI 1건을 뺀 수. 표시·숨김 열은 DOI 없는 ORCID 항목과 출처에서 다시 찾지 못한 기존 항목을 포함한다.)

## 4. 제외 사유별 개수

| 사유 | 건수 | 그중 저널 버전이 목록에 있음 |
|---|---|---|
| preprint | 46 | 20 |
| 학회 초록·발표(EGU/AGU 등) | 23 | - |
| dataset/software | 21 | - |
| erratum/correction/retraction | 8 | - |
| peer-review | 6 | - |
| supplementary | 4 | - |
| 기타 유형(학술지 논문 아님: book-chapter 등) | 2 | - |
| ORCID에 잘못 적힌 DOI(다른 논문, 올바른 DOI로 대체) | 1 | - |
| 합계 | 111 | |

<details><summary>제외 목록 전체</summary>

| DOI | 사유 | 출처 | 제목 | 저널 버전 |
|---|---|---|---|---|
| 10.5194/egusphere-egu2020-6491 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Two aspects of decadal ENSO variability modulating the long-term global carbon cycle |  |
| 10.5194/egusphere-egu2020-6492 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Mechanism of the Double peaked El Nino |  |
| 10.5194/egusphere-egu2020-6502 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Extensive fires in southeastern Siberian permafrost linked to preceding Arctic Oscillation |  |
| 10.5194/egusphere-egu22-10878 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Hysteresis of terrestrial carbon cycle to CO2 ramp-up and -down forcing |  |
| 10.5194/egusphere-egu22-10888 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | How to utilize deep learning to understand climate dynamics? : An ENSO example. |  |
| 10.5194/egusphere-egu22-10935 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Super recovery of the Hadley Cell edge to the CO2 removal |  |
| 10.5194/egusphere-egu22-10958 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Diverse Arctic Oscillation responses after volcanic eruptions at different latitudes during the last millenniu |  |
| 10.5194/egusphere-egu23-14677 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Increasing Arctic River Discharge and Its Role for the Phytoplankton Responses in the Present-day and Future C |  |
| 10.5194/egusphere-egu23-1664 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Irreversible changes in surface temperature and precipitation to CO2 forcing |  |
| 10.5194/egusphere-egu23-1944 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | ENSO-driven abrupt phase shift in North Atlantic Oscillation in early January |  |
| 10.5194/egusphere-egu23-1945 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Explosive increase in convective Extreme El Niño events in the CO2 removal scenario |  |
| 10.5194/egusphere-egu23-1960 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Two regimes of inter-basin interactions between the Atlantic and Pacific Oceans on interannual timescales |  |
| 10.5194/egusphere-egu23-2165 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Main drivers of Indian Ocean dipole asymmetry revealed by a simple IOD model |  |
| 10.5194/egusphere-egu24-21067 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | An abrupt shift in gross primary productivity over Eastern China-Mongolia and its inter-model diversity in lan |  |
| 10.5194/egusphere-egu24-21090 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | Fast recovery of North Atlantic sea level in response to atmospheric CO2 removal |  |
| 10.5194/egusphere-egu24-3737 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Arctic sea ice loss and La Niña as precursors of extreme East Asian cold winters |  |
| 10.5194/egusphere-egu24-4820 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Synchronous Decadal Climate Variability in the Tropical Central Pacific and Tropical South Atlantic |  |
| 10.5194/egusphere-egu25-2792 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | Asymmetric hysteresis response of mid-latitude storm tracks to CO2 removal |  |
| 10.5194/egusphere-egu25-3974 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Increased multi-year ENSO predictability under greenhouse gas warming accounted by large ensemble simulations  |  |
| 10.5194/egusphere-egu25-859 | 학회 초록·발표(EGU/AGU 등) | openalex,crossref | Reconciled warning signals in observations and models indicate a nearing AMOC tipping point |  |
| 10.5194/egusphere-egu26-16364 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | AI emulator highlights underestimated risk of AMOC collapse in current climate models |  |
| 10.5194/egusphere-egu26-8748 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | Seasonal Predictability of Antarctic Sea Ice based on Deep-learning Approach |  |
| 10.5194/egusphere-egu26-9260 | 학회 초록·발표(EGU/AGU 등) | orcid,openalex,crossref | Impact of Soil Moisture on Carbon Cycle Changes in Permafrost Regions in CESM2 |  |
| 10.5281/zenodo.18453259 | dataset/software | openalex | Data associated with: Precessional modulation of ENSO strength and spatial structure in a transient CGCM simul |  |
| 10.5281/zenodo.21352928 | dataset/software | openalex | Stratospheric Aerosol Injection Amplifies or Restores Future ENSO Variability Depending on Its Latitude |  |
| 10.5281/zenodo.21359650 | dataset/software | openalex | Stratospheric Aerosol Injection Location Controls Future ENSO Variability |  |
| 10.5281/zenodo.8176668 | dataset/software | openalex | Future tropical cyclone activity over the western North Pacific modulated by phytoplankton feedback under glob |  |
| 10.6084/m9.figshare.11924142 | dataset/software | openalex | Lagrangian Plankton Model |  |
| 10.6084/m9.figshare.14183072 | dataset/software | openalex | Idealized simulations with Antarctic meltwater |  |
| 10.6084/m9.figshare.16669324 | dataset/software | openalex | Data for "Hysteresis of the Intertropical Convergence Zone to CO2 Forcing" |  |
| 10.6084/m9.figshare.17194220 | dataset/software | openalex | DATA.zip |  |
| 10.6084/m9.figshare.19354055 | dataset/software | openalex | Data for "Centennial memory of the Arctic Ocean for future Arctic climate recovery in response to a carbon dio |  |
| 10.6084/m9.figshare.21802923 | dataset/software | openalex | North Pacific Oscillation influence on tropical variability through stationary wave energy propagation |  |
| 10.6084/m9.figshare.22637329 | dataset/software | openalex | Data for "Role of Atlantification in future changes in Arctic primary productivity" |  |
| 10.6084/m9.figshare.23266058 | dataset/software | openalex | Data for "Increase in convective Extreme El Niño events in a CO2 removal scenario" |  |
| 10.6084/m9.figshare.23266265 | dataset/software | openalex | Data for "How will global carbon cycle respond to negative emissions?" |  |
| 10.6084/m9.figshare.23916513 | dataset/software | openalex | Mutating ENSO impact on Northwest Pacific tropical cyclones under global warming |  |
| 10.6084/m9.figshare.24325073 | dataset/software | openalex | Potential intensification of permafrost carbon feedback under net-zero and negative emissions |  |
| 10.6084/m9.figshare.24453214 | dataset/software | openalex | Data for ["Delayed ENSO impact on phytoplankton variability over the Western North Pacific"] |  |
| 10.6084/m9.figshare.30100513 | dataset/software | openalex | Background atmospheric CO2 regulates the local and non-local climate impacts of Amazon deforestation |  |
| 10.6084/m9.figshare.31173886 | dataset/software | openalex | Soil Moisture Controls on Permafrost Carbon Cycle under Greenhouse Warming and Zero Emission Pathways |  |
| 10.6084/m9.figshare.31898308 | dataset/software | openalex | Data and codes for "Hemispheric contrast in summer season duration responses to CO2 removal" |  |
| 10.6084/m9.figshare.5053930 | dataset/software | openalex | Data for "Reduced North American terrestrial primary productivity linked to anomalous Arctic warming" |  |
| 10.6084/m9.figshare.5053948 | dataset/software | openalex | Code for "Reduced North American terrestrial primary productivity linked to anomalous Arctic warming" |  |
| 10.1007/s00382-011-1122-1 | erratum/correction/retraction | orcid,openalex,crossref | Erratum to: Transformed eddy-PV flux and positive synoptic eddy feedback onto low-frequency flow |  |
| 10.1007/s13143-015-0072-7 | erratum/correction/retraction | orcid,openalex,crossref | Erratum to: Changes in weather and climate extremes over Korea and possible causes: A review |  |
| 10.1038/nature08546 | erratum/correction/retraction | orcid,openalex,crossref | Erratum: El Niño in a changing climate |  |
| 10.1038/s41467-017-02461-9 | erratum/correction/retraction | orcid,openalex,crossref | Author Correction: Intensification of terrestrial carbon cycle related to El Niño–Southern Oscillation under g |  |
| 10.1038/s41467-025-55918-7 | erratum/correction/retraction | orcid,openalex,crossref | Author Correction: Pervasive fire danger continued under a negative emission scenario |  |
| 10.1038/s41586-019-0994-9 | erratum/correction/retraction | orcid,openalex,crossref | Author Correction: El Niño–Southern Oscillation complexity |  |
| 10.1088/1748-9326/7/3/039502 | erratum/correction/retraction | orcid,openalex,crossref | Corrigendum: Improved simulation of two types of El Niño in CMIP5 models |  |
| 10.1175/2010jcli3778.1 | erratum/correction/retraction | orcid,openalex,crossref | CORRIGENDUM |  |
| 10.1175/jcli-d-11-00696.1 | ORCID에 잘못 적힌 DOI(다른 논문, 올바른 DOI로 대체) |  | An Enhanced Influence of Tropical Indian Ocean on the South Asia High after the Late 1970s | 10.1175/jcli-d-12-00078.1 |
| 10.1002/9781119548164.ch11 | 기타 유형(학술지 논문 아님: book-chapter 등) | openalex,crossref | ENSO Remote Forcing |  |
| 10.1002/9781119548164.ch4 | 기타 유형(학술지 논문 아님: book-chapter 등) | openalex,crossref | ENSO Diversity |  |
| 10.5194/egusphere-2024-3406-ac1 | peer-review | openalex,crossref | Reply on RC2 |  |
| 10.5194/egusphere-2024-3406-ac2 | peer-review | openalex,crossref | Reply on RC3 |  |
| 10.5194/egusphere-2024-3406-ac3 | peer-review | openalex,crossref | Reply on RC1 |  |
| 10.5194/egusphere-2024-3406-ac4 | peer-review | openalex,crossref | Reply on RC4 |  |
| 10.5194/egusphere-2025-1474-ac1 | peer-review | openalex,crossref | Reply on RC2 |  |
| 10.5194/egusphere-2025-1474-ac2 | peer-review | openalex,crossref | Reply on RC1 |  |
| 10.1002/essoar.10502935.1 | preprint | orcid,openalex,crossref | Impact of Antarctic meltwater forcing on East Asian climate under greenhouse warming | 10.1029/2020gl089951 |
| 10.1002/essoar.10503236.1 | preprint | orcid,crossref | Diversity of Pacific Meridional Mode and its distinct impacts on El Niño-Southern Oscillation | 10.1029/2020gl088993 |
| 10.1002/essoar.10505532.1 | preprint | orcid,openalex,crossref | Tropical drivers of interannual vegetation variability in eastern Africa |  |
| 10.1002/essoar.10510239.1 | preprint | orcid,crossref | The Route to Spring Phytoplankton Blooms Simulated by a Lagrangian Plankton Model | 10.1029/2020jc016753 |
| 10.1002/essoar.10510807.1 | preprint | orcid,crossref | Increasing Arctic River Discharge and Its Role for the Phytoplankton Responses in the Present and Future Clima |  |
| 10.21203/rs.3.rs-10574165/v1 | preprint | openalex,crossref | Weakening Boundary Layer-Lower-Free-Troposphere coupling limits ENSO Amplification under Global Warming |  |
| 10.21203/rs.3.rs-1074581/v1 | preprint | orcid,crossref | Hysteresis of terrestrial carbon cycle to CO2 ramp-up and -down forcing |  |
| 10.21203/rs.3.rs-144842/v1 | preprint | crossref | Tropical Drivers of Interannual Vegetation Variability in Eastern Africa |  |
| 10.21203/rs.3.rs-146325/v1 | preprint | openalex,crossref | WITHDRAWN: Asymmetrical response of summer rainfall in East Asia to CO2 forcing | 10.1016/j.scib.2021.08.013 |
| 10.21203/rs.3.rs-1750497/v1 | preprint | orcid,crossref | How does the North Pacific Oscillation affect tropical variability? Part I: Role of Stationary Wave Propagatio |  |
| 10.21203/rs.3.rs-1750550/v1 | preprint | orcid,crossref | How does the North Pacific Oscillation affect tropical variability? Part II: Intermodel diversity in the NPO-E |  |
| 10.21203/rs.3.rs-1938270/v1 | preprint | orcid,openalex,crossref | Explosive increase in convective Extreme El Niño events in the CO2 removal scenario | 10.1126/sciadv.adh2412 |
| 10.21203/rs.3.rs-2238154/v1 | preprint | orcid,crossref | ENSO-driven abrupt phase shift in North Atlantic Oscillation in early January | 10.1038/s41612-023-00414-2 |
| 10.21203/rs.3.rs-241280/v1 | preprint | crossref | Irreversible Response of the Intertropical Convergence Zone (ITCZ) to CO2 Forcing |  |
| 10.21203/rs.3.rs-2435609/v1 | preprint | crossref | Intermodel relation between present-day warm pool intensity and future precipitation changes | 10.1007/s00382-023-06918-0 |
| 10.21203/rs.3.rs-2578164/v1 | preprint | crossref | Distinct decadal modulation of Atlantic-Niño influence on ENSO | 10.1038/s41612-023-00429-9 |
| 10.21203/rs.3.rs-2932237/v1 | preprint | orcid,crossref | Midwinter Breakdown of ENSO Climate Impacts in East Asia | 10.1038/s41612-023-00474-4 |
| 10.21203/rs.3.rs-3010327/v1 | preprint | orcid,openalex,crossref | An abrupt shift in gross primary productivity over Eastern China-Mongolia |  |
| 10.21203/rs.3.rs-3176943/v1 | preprint | orcid,openalex,crossref | Negative CO2 emissions mitigate extremes of the terrestrial hydrological cycle via a vegetation physiological  |  |
| 10.21203/rs.3.rs-335202/v1 | preprint | crossref | Impacts of ENSO On The Seasonal Transition From Summer to Winter in East Asia | 10.1007/s00382-021-06019-w |
| 10.21203/rs.3.rs-3376707/v1 | preprint | openalex,crossref | Emergence of the South Atlantic Convergence Zone–ENSO connection under global warming |  |
| 10.21203/rs.3.rs-3613787/v1 | preprint | crossref | Future changes in the wintertime ENSO-NAO teleconnection under greenhouse warming | 10.1038/s41612-024-00627-z |
| 10.21203/rs.3.rs-3827037/v1 | preprint | orcid,openalex,crossref | North Atlantic chlorophyll blooms enhance terrestrial primary productivity over Europe |  |
| 10.21203/rs.3.rs-3831926/v1 | preprint | crossref | Delayed recovery of Atlantic meridional ocean circulation threatens Europe-wide gross primary productivity und |  |
| 10.21203/rs.3.rs-3835620/v1 | preprint | orcid,openalex,crossref | Hysteresis in ENSO teleconnections under a CO2 removal pathway |  |
| 10.21203/rs.3.rs-3884587/v1 | preprint | openalex,crossref | Emergence of the ocean CO2 uptake hole under global warming | 10.1038/s41467-025-57724-7 |
| 10.21203/rs.3.rs-3935615/v1 | preprint | orcid,openalex,crossref | Intensified Responses of Phytoplankton to the Indian Ocean Dipole Under Greenhouse Warming |  |
| 10.21203/rs.3.rs-4161623/v1 | preprint | orcid,crossref | Fast recovery of North Atlantic sea level in response to atmospheric CO2 removal | 10.1038/s43247-024-01835-4 |
| 10.21203/rs.3.rs-420092/v1 | preprint | openalex,crossref | The Role of SST in Explaining the Economic Growth of Indian Ocean Countries |  |
| 10.21203/rs.3.rs-4531524/v1 | preprint | orcid,crossref | Significant Winter Atlantic Niño effect on ENSO and its future projection | 10.1038/s41612-024-00790-3 |
| 10.21203/rs.3.rs-4812859/v1 | preprint | openalex,crossref | Siberian Greening Enhances Coastal Spring Chlorophyll in Western North America |  |
| 10.21203/rs.3.rs-5942136/v1 | preprint | crossref | Arctic stratospheric ozone as a precursor of ENSO events since 2000s | 10.1038/s41612-025-01220-8 |
| 10.21203/rs.3.rs-7757839/v1 | preprint | openalex,crossref | Relationship between Pacific–South America teleconnections in austral fall and ENSO evolution |  |
| 10.21203/rs.3.rs-9329627/v1 | preprint | openalex,crossref | Rainfall dynamics in Sri Lanka: A Review of Present Variability, Trends and Responses to Climate Change |  |
| 10.21203/rs.3.rs-966527/v1 | preprint | crossref | Tropical Origins of the Record-breaking 2020 Summer Rainfall Extremes in East Asia | 10.1038/s41598-022-09297-4 |
| 10.22541/essoar.168676907.79589211/v1 | preprint | orcid,openalex,crossref | How will global carbon cycle respond to negative emissions? |  |
| 10.22541/essoar.169945520.09413182/v1 | preprint | orcid,openalex,crossref | Non-monotonic responses of Atlantic Meridional Overturning Circulation to Antarctic meltwater forcing |  |
| 10.22541/essoar.170000399.94972609/v1 | preprint | orcid,openalex,crossref | A biological dipole variability in the Indian Ocean | 10.1088/1748-9326/ad1641 |
| 10.22541/essoar.172191630.08428230/v1 | preprint | crossref | The El Niño Southern Oscillation (ENSO) recharge oscillator conceptual model : achievements and future prospec | 10.1029/2024rg000843 |
| 10.31223/x52t56 | preprint | crossref | Evaluation and prediction of the Effects of Planetary Orbital Variations to Earth’s Temperature Changes | 10.1080/17538947.2025.2487058 |
| 10.48550/arxiv.2609.18551 | preprint | openalex | Disentangled Fingerprints suggest no historical weakening of Atlantic Overturning and Subpolar Gyre |  |
| 10.5194/acp-2022-187 | preprint | openalex,crossref | How volcanic eruption latitudes diversify surface climate responses |  |
| 10.5194/egusphere-2024-3406 | preprint | orcid,crossref | Two different phytoplankton blooming mechanisms over the East China Sea during El-Niño decaying summers |  |
| 10.5194/egusphere-2025-1474 | preprint | orcid,crossref | Hysteresis of phytoplankton communities over Sub-polar North Atlantic to CO2 forcing |  |
| 10.5194/egusphere-2026-1556 | preprint | orcid,openalex,crossref | Seasonal Predictability of Antarctic Sea Ice based on a Deep-learning Approach |  |
| 10.5194/egusphere-2026-353 | preprint | orcid,crossref | Regional contrasts of ecosystem productivity sensitivity to atmospheric CO2 growth across East Asia | 10.5194/esd-17-1381-2026 |
| 10.5194/acp-2022-187-supplement | supplementary | openalex,crossref | Supplementary material to "How volcanic eruption latitudes diversify surface climate responses" |  |
| 10.5194/egusphere-2024-3406-supplement | supplementary | orcid,openalex,crossref | Supplementary material to "Two different phytoplankton blooming mechanisms over the East China Sea during El-N |  |
| 10.5194/egusphere-2025-1474-supplement | supplementary | orcid,openalex,crossref | Supplementary material to "Hysteresis of phytoplankton communities over Sub-polar North Atlantic to CO2 forcin |  |
| 10.5194/egusphere-2026-1556-supplement | supplementary | orcid,openalex,crossref | Supplementary material to "Seasonal Predictability of Antarctic Sea Ice based on a Deep-learning Approach" |  |

</details>

## 5. needs_review 목록 (1편, 화면에서 숨김)

| DOI | 연도 | 제목 | 출처 | 사유 |
|---|---|---|---|---|
| [10.1175/bams-eee_2014_ch20.1](https://doi.org/10.1175/bams-eee_2014_ch20.1) | 2015 | Human Contribution to the 2014 Record High Sea Surface Temperatures Over the Western Tropical And Northeast Pa | crossref | 같은 제목의 다른 DOI 존재(10.1175/bams-d-15-00055.1) |

### 5-1. Reply/Comment (0편)

| DOI | 연도 | 학술지 | 제목 |
|---|---|---|---|

## 6. 단일 출처 목록 (표시 중 0편)

Crossref 저자 확인(family=Kug, 이름 Jong-Seong/J.-S. 계열)과 유형 확인을 통과해 표시한다.

| DOI | 연도 | 학술지 | 제목 | 출처 |
|---|---|---|---|---|

## 7. 연도별 편수

| 연도 | 표시 | 숨김 | 표시 중 ORCID | 표시 중 OpenAlex | 표시 중 Crossref검색 | OpenAlex article+review(원자료) |
|---|---|---|---|---|---|---|
| 2026 | 19 | 0 | 16 | 19 | 19 | 20 |
| 2025 | 21 | 0 | 14 | 21 | 21 | 21 |
| 2024 | 29 | 0 | 24 | 29 | 29 | 26 |
| 2023 | 23 | 0 | 15 | 23 | 23 | 26 |
| 2022 | 27 | 0 | 13 | 27 | 27 | 23 |
| 2021 | 19 | 0 | 6 | 19 | 19 | 21 |
| 2020 | 10 | 0 | 8 | 10 | 10 | 11 |
| 2019 | 8 | 0 | 8 | 8 | 8 | 9 |
| 2018 | 9 | 0 | 9 | 9 | 9 | 8 |
| 2017 | 9 | 0 | 9 | 9 | 9 | 10 |
| 2016 | 11 | 0 | 10 | 11 | 11 | 23 |
| 2015 | 16 | 1 | 15 | 16 | 16 | 32 |
| 2014 | 15 | 0 | 14 | 15 | 15 | 16 |
| 2013 | 14 | 0 | 13 | 14 | 14 | 30 |
| 2012 | 16 | 0 | 16 | 16 | 16 | 19 |
| 2011 | 15 | 0 | 15 | 15 | 15 | 23 |
| 2010 | 18 | 0 | 18 | 18 | 18 | 28 |
| 2009 | 11 | 0 | 11 | 11 | 11 | 18 |
| 2008 | 9 | 0 | 9 | 9 | 8 | 16 |
| 2007 | 3 | 0 | 3 | 3 | 3 | 13 |
| 2006 | 4 | 0 | 4 | 4 | 4 | 16 |
| 2005 | 4 | 0 | 4 | 4 | 4 | 11 |
| 2004 | 2 | 0 | 2 | 2 | 2 | 5 |
| 2003 | 2 | 0 | 2 | 2 | 2 | 7 |
| 2002 | 1 | 0 | 1 | 1 | 1 | 3 |
| 2001 | 1 | 0 | 1 | 1 | 1 | 3 |
| 2000 | 1 | 0 | 1 | 1 | 1 | 1 |
| 합계 | 317 | 1 | 261 | 317 | 316 | 440 |

- 2017, 2018, 2019, 2020년 편수가 적다. 이 기간은 ORCID·OpenAlex·Crossref 저자 검색(성 Kug 전수 조회)이 모두 같은 논문만 보여 주고, 단일 출처 항목이 없다. 이름 변형으로 갈라진 OpenAlex ID는 2개(각 1건, DOI 없음)뿐이라 누락보다는 실제 출판 수로 보인다.
- OpenAlex 원자료 열이 2005~2016년에 큰 것은 DOI 없는 학회 초록(한국기상학회 학술대회 논문집 등)이 article로 분류돼 있기 때문이다(10-1절).

## 8. 출처 간 연도·학술지 불일치

연도는 `pubtools.pub_date` 규칙(published-print 우선)으로 정한 값이 기준이다. 온라인 선공개와 인쇄 연도 차이가 대부분이다.

### 8-1. 연도 불일치 63편

<details><summary>목록</summary>

| DOI | 채택 연도 | ORCID | OpenAlex | 표시 |
|---|---|---|---|---|
| 10.1002/2015gl066864 | 2016 | 2016 | 2015 | 표시 |
| 10.1002/joc.1774 | 2009 | 2009 | 2008 | 표시 |
| 10.1002/joc.2163 | 2011 | 2011 | 2010 | 표시 |
| 10.1002/joc.2329 | 2012 | 2012 | 2011 | 표시 |
| 10.1002/joc.6772 | 2021 | - | 2020 | 표시 |
| 10.1007/s00382-007-0264-7 | 2008 | 2008 | 2007 | 표시 |
| 10.1007/s00382-007-0310-5 | 2008 | 2008 | 2007 | 표시 |
| 10.1007/s00382-007-0348-4 | 2008 | 2008 | 2007 | 표시 |
| 10.1007/s00382-008-0434-2 | 2009 | 2009 | 2008 | 표시 |
| 10.1007/s00382-008-0460-0 | 2009 | 2009 | 2008 | 표시 |
| 10.1007/s00382-008-0483-6 | 2009 | 2009 | 2008 | 표시 |
| 10.1007/s00382-009-0586-8 | 2010 | 2010 | 2009 | 표시 |
| 10.1007/s00382-009-0606-8 | 2010 | 2010 | 2009 | 표시 |
| 10.1007/s00382-009-0664-y | 2010 | 2010 | 2009 | 표시 |
| 10.1007/s00382-010-0873-4 | 2011 | 2011 | 2010 | 표시 |
| 10.1007/s00382-010-0912-1 | 2011 | 2011 | 2010 | 표시 |
| 10.1007/s00382-010-0913-0 | 2011 | 2011 | 2010 | 표시 |
| 10.1007/s00382-011-1142-x | 2012 | 2012 | 2011 | 표시 |
| 10.1007/s00382-011-1157-3 | 2012 | 2012 | 2011 | 표시 |
| 10.1007/s00382-011-1171-5 | 2012 | 2012 | 2011 | 표시 |
| 10.1007/s00382-012-1420-2 | 2013 | 2013 | 2012 | 표시 |
| 10.1007/s00382-012-1477-y | 2013 | 2013 | 2012 | 표시 |
| 10.1007/s00382-012-1630-7 | 2013 | 2013 | 2012 | 표시 |
| 10.1007/s00382-012-1640-5 | 2014 | 2014 | 2013 | 표시 |
| 10.1007/s00382-013-2008-1 | 2014 | 2014 | 2013 | 표시 |
| 10.1007/s00382-013-2009-0 | 2014 | 2014 | 2013 | 표시 |
| 10.1007/s00382-014-2349-4 | 2015 | 2015 | 2014 | 표시 |
| 10.1007/s00382-015-2776-x | 2016 | 2016 | 2015 | 표시 |
| 10.1007/s00382-015-2799-3 | 2016 | 2016 | 2015 | 표시 |
| 10.1007/s00382-015-2833-5 | 2016 | 2016 | 2015 | 표시 |
| 10.1007/s00382-016-3121-8 | 2017 | 2017 | 2016 | 표시 |
| 10.1007/s00382-016-3303-4 | 2017 | 2017 | 2016 | 표시 |
| 10.1007/s00382-016-3339-5 | 2017 | 2017 | 2016 | 표시 |
| 10.1007/s00382-016-3402-2 | 2017 | 2017 | 2016 | 표시 |
| 10.1007/s00382-016-3473-0 | 2019 | 2019 | 2016 | 표시 |
| 10.1007/s00382-016-3474-z | 2017 | 2017 | 2016 | 표시 |
| 10.1007/s00382-017-3779-6 | 2018 | 2018 | 2017 | 표시 |
| 10.1007/s00382-017-4036-8 | 2018 | 2018 | 2017 | 표시 |
| 10.1007/s00382-018-4450-6 | 2019 | 2019 | 2018 | 표시 |
| 10.1007/s00382-021-06019-w | 2022 | - | 2021 | 표시 |
| 10.1007/s00382-023-06918-0 | 2024 | 2024 | 2023 | 표시 |
| 10.1007/s00704-008-0067-8 | 2009 | 2009 | 2008 | 표시 |
| 10.1007/s00704-009-0183-0 | 2010 | 2010 | 2009 | 표시 |
| 10.1007/s00704-013-1045-3 | 2014 | 2014 | 2013 | 표시 |
| 10.1007/s13143-014-0013-x | 2014 | 2014 | 2013 | 표시 |
| 10.1007/s13143-019-00146-5 | 2020 | 2020 | 2019 | 표시 |
| 10.1016/j.atmosres.2008.10.022 | 2009 | 2009 | 2008 | 표시 |
| 10.1016/j.scib.2021.08.013 | 2022 | - | 2021 | 표시 |
| 10.1029/2011gl050005 | 2012 | 2012 | 2011 | 표시 |
| 10.1029/2023gl105864 | 2024 | 2024 | 2023 | 표시 |
| 10.1038/s41558-017-0033-5 | 2018 | 2018 | 2017 | 표시 |
| 10.1038/s41558-021-01211-6 | 2022 | 2022 | 2021 | 표시 |
| 10.1088/1748-9326/ac444e | 2022 | 2022 | 2021 | 표시 |
| 10.1088/1748-9326/ad1641 | 2024 | 2024 | 2023 | 표시 |
| 10.1175/2008jcli2624.1 | 2009 | 2009 | 2008 | 표시 |
| 10.1175/2009jcli2894.1 | 2010 | 2010 | 2009 | 표시 |
| 10.1175/2009jcli2895.1 | 2010 | 2010 | 2009 | 표시 |
| 10.1175/2009jcli3293.1 | 2010 | 2010 | 2009 | 표시 |
| 10.1175/jcli-d-13-00084.1 | 2014 | 2014 | 2013 | 표시 |
| 10.1175/jcli-d-14-00376.1 | 2015 | 2015 | 2014 | 표시 |
| 10.1175/jcli-d-15-0406.1 | 2016 | 2016 | 2015 | 표시 |
| 10.1175/jcli-d-19-0364.1 | 2020 | 2020 | 2019 | 표시 |
| 10.1175/jcli-d-20-0402.1 | 2021 | - | 2020 | 표시 |

</details>

### 8-2. 학술지명 불일치 2건 (한쪽이 다른 쪽을 포함하는 부분 일치 9건은 제외)

<details><summary>목록</summary>

| DOI | Crossref | 출처 | 출처 표기 |
|---|---|---|---|
| 10.1029/2002jc001671 | Journal of Geophysical Research: Oceans | openalex | Journal of Geophysical Research Atmospheres |
| 10.3402/tellusa.v65i0.19863 | Tellus A: Dynamic Meteorology and Oceanography | orcid | Tellus, Series A: Dynamic Meteorology and Oceanography |

</details>

## 9. 무작위 10편 Crossref 재조회 일치 확인

표시 논문 중 무작위 10편(seed 20261103)을 캐시 없이 Crossref에서 다시 받아 `crossref_to_entry` 결과와 yaml 값을 비교했다(title, authors, journal, year, date, volume, issue, pages). **일치 10/10**

| DOI | 연도 | 결과 | 다른 필드 |
|---|---|---|---|
| 10.1007/s00382-015-2833-5 | 2016 | 일치 | - |
| 10.1007/s13143-013-0016-z | 2013 | 일치 | - |
| 10.1016/j.accre.2022.07.001 | 2022 | 일치 | - |
| 10.1029/2002gl015983 | 2003 | 일치 | - |
| 10.63737/jhl.25.0024 | 2025 | 일치 | - |
| 10.1007/s00704-009-0183-0 | 2010 | 일치 | - |
| 10.1007/s00382-010-0912-1 | 2011 | 일치 | - |
| 10.1175/jcli-d-11-00303.1 | 2012 | 일치 | - |
| 10.1029/2012gl053305 | 2012 | 일치 | - |
| 10.1175/jcli-d-12-00078.1 | 2012 | 일치 | - |

## 10. ORCID DOI 점검·DOI 없는 항목 처리

ORCID 제목과 Crossref 제목이 크게 다른(유사도 < 0.75) DOI는 ORCID 제목으로 Crossref를 다시 검색해 정정했다.

| ORCID DOI | 정정 DOI | ORCID 제목 | Crossref 제목(ORCID DOI) |
|---|---|---|---|
| 10.1175/jcli-d-11-00696.1 | 10.1175/jcli-d-12-00078.1 | Indian ocean feedback to the ENSO transition in a multimodel ensemble | An Enhanced Influence of Tropical Indian Ocean on the South Asia High after the  |

| 제목 | 학술지 | 연도 | 처리 |
|---|---|---|---|
| Optimal multi-model ensemble method in seasonal climate prediction | Asia-Pacific Journal of Atmospheric Sciences | 2008 | DOI 없이 ORCID 메타데이터로 포함 |
| Symmetric and antisymmetric mass exchanges between the equatorial and off-equatorial Pacific associa | Journal of Geophysical Research C: Oceans | 2003 | DOI 항목과 같은 논문 → 10.1029/2002jc001671 에 병합 |

### 10-1. OpenAlex의 DOI 없는 article 123건 (규칙상 미포함)

- 이미 목록에 있는 논문과 제목이 같음: 4건
- 학회 초록집(한국기상학회 학술대회 논문집, AGU/EGU 등): 106건
- 그 밖의 항목 13건 — 국내 학술지 논문일 수 있어 사람 확인이 필요하다(ORCID에 없어서 넣지 않음):

| OpenAlex | 연도 | 출처 표기 | 제목 | 저자(앞 3명) |
|---|---|---|---|---|
| W2233149770 | 2001 | 대기 | A Study of ENSO predictability in KMA/SNU Model | Jong‐Seong Kug; In‐Sik Kang; Stephen E. Zebiak |
| W2199928003 | 2001 | 대기 | Asymmetric Characteristics of Mass Exchnage Associated with ENSO in Northern and Southern  | Jong‐Seong Kug; In‐Sik Kang; Soon‐Il An |
| W2290943417 | 2002 | 대기 | A Nearly Annual Coupled Mode in the Equatorial Pacific Ocean | Jong‐Seong Kug; In‐Sik Kang; Fei‐Fei Jin |
| W2202577080 | 2002 | 대기 | Iterative Wind Stress Correction for SST Simulation in OGCM | Hui-Je Cho; Jong‐Seong Kug; In‐Sik Kang |
| W2255745437 | 2003 | 대기 | A Nearly Annual Mode in the tropical Pacific | Jong‐Seong Kug; In‐Sik Kang; Fei‐Fei Jin |
| W2244323293 | 2003 | 대기 | A Theory for the Nearly Annual Mode in the tropical Pacific | Jong‐Seong Kug; In‐Sik Kang; Fei‐Fei Jin |
| W2271565334 | 2003 | 대기 | Global SST Prediction with a Dynamical-Statistical Prediction System | June‐Yi Lee; In‐Sik Kang; Jong‐Seong Kug |
| W2265106482 | 2003 | 대기 | Intermittent Interaction between the ENSO and Indian Ocean | Jong‐Seong Kug; Yoo‐Geun Ham; In‐Sik Kang |
| W2215134306 | 2003 | 대기 | Western Pacific SST Prediction with an intermediate coupled Model | Jong‐Seong Kug; In‐Sik Kang |
| W1916742489 | 2010 | - | Ocean Dynamic Processes Responsible for the Interannual Variability of the Tropical Indian | Jong‐Seong Kug; Soon‐Il An |
| W2585954984 | 2015 | - | Characteristics of predictable MJOs | H. M. Kim; D. Kim; Frédéric Vitart |
| W2898124896 | 2015 | - | Climate model biases and El Niño Southern Oscillation (ENSO) simulation | Antonietta M. Capotondi; Yoo‐Geun Ham; Andrew T. Wittenberg |
| W3187381339 | 2020 | Geophysical Research Letters | 長期全球炭素循環を調節する10年ENSO変動の2つの側面【JST・京大機械翻訳】 | Park So-Won; Jin‐Soo Kim; Kug Jong-Seong |

## 11. 기존 항목·수동 필드 보존

- 보존한 수동 필드: corresponding 5건, featured 5건
- 출처에서 다시 찾지 못해 그대로 둔 기존 항목: 0건

## 12. 규칙·한계

- 포함: Crossref type `journal-article`(리뷰 포함) + 저자 목록에 family=Kug(이름 J로 시작). DOI 없는 ORCID 학술지 논문은 ORCID 메타데이터로 포함.
- 제외: DOI 접두어(10.21203, 10.22541, 10.1002/essoar, 10.48550, 10.5194 토론·EGUsphere·EGU 초록, 10.5281 등), Crossref type(posted-content, peer-review, component, dataset, proceedings 등), `update-to`가 있거나 제목이 Correction/Erratum/Corrigendum/Retraction인 것, 기타 유형(book-chapter 등). Crossref 미등록이면 OpenAlex 유형으로 판정.
- needs_review: 저자 확인 실패·애매, Reply/Comment, Crossref 미등록, 같은 제목의 다른 DOI. `review_reason`에 사유를 적는다 (다시 실행하면 다시 계산). `review_reason` 없이 사람이 넣은 `needs_review`(true/false)는 보존한다.
- 저자 검색의 한계: Crossref에 저자 성이 뒤바뀌어 등록된 논문(given=Kug)은 needs_review로 둔다. OpenAlex는 API 키 없이 공유 일일 예산으로 조회하므로 캐시(1일)를 둔다.

## 13. 사람이 확인할 점

1. needs_review 1편(5절): 확인 후 표시하려면 `needs_review: false`로 바꾸고 `review_reason` 줄을 지운다. `review_reason`이 없는 `needs_review`(true/false)는 사람이 정한 값으로 보고 다음 실행에서도 보존한다.
2. DOI 없이 ORCID 메타데이터로 넣은 항목 1편: 저자·권호를 원문과 대조한다 — Optimal multi-model ensemble method in seasonal climate pred (저자 Kug, J.-S., Lee, J.-Y., Kang, I.-K., Wang, B., Park, C.-K.).
3. OpenAlex에만 있는 DOI 없는 항목 13건(10-1절): 국내 학술지(예: 「대기」) 논문이면 직접 추가한다.
4. ORCID 기록의 DOI 오기 1건(10절): 교수님 ORCID에서 고치면 다음 수집부터 정상 반영된다.
5. 학술지 논문이 아니라 제외한 책 장(book chapter 등) 2건: 10.1002/9781119548164.ch11, 10.1002/9781119548164.ch4 — 별도 목록이 필요하면 알려 달라.
6. Reply/Comment 0편.

수정 금지 파일(build.py·validate.py·sitelib.py 등)에서 이번 작업에 영향을 준 버그는 찾지 못했다. 참고: `validate.py`의 selected_dois 검사는 목록에 있는지만 보고 숨김 여부는 보지 않는다(이 스크립트가 표시 여부를 assert한다). `pubtools.http_json`은 404에도 재시도해 실패당 약 6초를 기다린다(동작은 바꾸지 않음).

## 백업 대조

- 작성: 2026-11-04 · 원본 홈페이지 백업(`backup/`)의 논문 목록 ↔ `data/publications.yaml` (Task 7)
- 결과: **표시 318편**(317 → +1), 숨김 1편, yaml 전체 319편 · 추가 1 · 숨김 전환 1(이미 숨겨져 있던 needs_review → hidden, 표시 수 변화 없음) · `corresponding: true` 신규 53(전체 58) · `corr_authors` 56편 · needs_review 1 → 0
- `validate.py --data-only` 오류 0 (경고: 숨김 1건, 다른 작업의 placeholder 8건). `build.py`는 돌리지 않았다.

### B-1. 원본 자료와 대조 요약

원본 사이트(2026-10 캐시)는 "전체 317"편이지만 백업에서 읽을 수 있는 것은 **282행**뿐이다.

| 원본 자료 | 시점 | 행 | 사이트 번호 | 교신저자 표시 |
|---|---|---|---|---|
| 캐시 `wp-rocket/climate.snu.ac.kr/publication/index-https.html` | 2026-10 | 20 | No.298–317 (목록 1쪽만 캐시됨, 2~16쪽 없음) | 저자 뒤 `*` |
| DB KBoard board 3 (`kboard_board_content` + `kboard_board_option.doi_url`) | 2024-04-09 | 262 | No.1–262 | 제목 끝 `(CA)` (2009–2016년 논문 일부) |
| (없음) | 2024-04 ~ 2025 | **35** | **No.263–297** | - |

- 다른 도메인 캐시(`csl.postech.ac.kr` 262편 중 1쪽, `csl1234.cafe24.com`·`post.amongsoftware.gethompy.com` 190편 중 1쪽)도 모두 DB 범위 안이라 공백을 메우지 못한다. 현재 사이트는 HTTP 403, 웨이백 머신 보관본도 없다.
- 백업 안 다른 곳(구성원 상세 페이지 등)의 별표 표기는 쓰지 않았다(원본 = 논문 게시판).

| 구분 | 원본 행 | 우리 편 | 내용 |
|---|---|---|---|
| 일치 | 274 | 267 | DOI 일치 242행 + 제목 일치 32행(원본 DOI가 다른 논문을 가리킴 19, DOI 오타·비DOI 링크 등 13). 원본 안 중복 7쌍(B-4) |
| 원본만 | 8 | - | 추가 1(DOI 없는 국내 학술지), 규칙상 제외 7(정오표 3, preprint 2, 학회 초록 2) — B-2 |
| 우리만 | - | 51 | 백업 공백 구간 35, 캐시 이후 출판 6, 원본 누락 추정 8, 원본 표기 오류 1, 중복 DOI 1 — B-3. 51편 모두 Crossref에 Kug 저자 확인 → 오귀속 확실 0 |
| 합계 | 282 | 318 | 대조 시점 우리 목록(표시 317 + 숨김 1) |

- 맞추는 규칙: DOI 정규화(소문자, `doi.org/` 제거) 일치 → 없거나 제목이 크게 다르면(유사도 < 0.6) 제목 유사도(≥ 0.85, 연도 ±1; ≥ 0.95면 ±2). 제목이 `Author Correction / Erratum / Corrigendum`이면 정오표로 따로 분류.
- `add_publication.py`는 쓰지 않았다: 원본에만 있는 학술지 DOI 논문이 없었다(원본만 8행 중 DOI가 있는 7행은 모두 정오표·preprint·초록).
### B-2. 원본에만 있는 항목 (8행)

| 원본 | 연도 | 저자(원본) | 제목(원본) | 원본 DOI | 처리 | 근거 |
|---|---|---|---|---|---|---|
| DB uid 14790 | 2010 | Kug J.-S. and An, S.-I. | Ocean dynamic processes responsible for the interannual var… | `https://www.koreascience.or.kr/article/…` | **추가** | DOI 없음(Crossref 제목 검색 실패). 「대기」(Atmosphere) 20(2) 211-219, OpenAlex W1916742489로 권·호·쪽 확인 → 직접 입력(`source: backup`) |
| DB uid 14910 | 2018 | Kim, J.-S., Kug, J.-S., & Jeong, S.-J. | Author Correction: Intensification of terrestrial carbon cy… | 10.1038/s41467-017-02461-9 | 제외 | 정오표(Author Correction). 본 논문 10.1038/s41467-017-01831-7 은 목록에 있음 |
| DB uid 14913 | 2019 | Timmermann, A., An, S.-I., Kug, J.-S., … | Author Correction: El Niño–Southern Oscillation complexity.… | 10.1007/s00382-018-4450-6 | 제외 | 정오표(Author Correction: ENSO complexity, 실제 DOI 10.1038/s41586-019-0994-9). 원본 링크는 인접 항목 DOI로 잘못 연결. 본 논문 10.1038/s41586-018-0252-6 은 목록에 있음 |
| DB uid 14914 | 2015 | Min, S.-K., Son, S.-W., Seo, K.-H., Kug… | Erratum to: Changes in weather and climate extremes over Ko… | 10.1007/s13143-015-0072-7 | 제외 | 정오표(Erratum). 본 논문 10.1007/s13143-015-0066-5 는 목록에 있음 |
| DB uid 14943 | 2022 | Park J., Kim S., Lim, H.-G., Kug, J.-S.… | Increasing Arctic River Discharge and Its Role for the Phyt… | 10.1002/essoar.10510807.1 | 제외 | preprint(ESSOAr). Crossref is-preprint-of → 10.1088/1748-9326/acd568 (목록에 있음, 원본 DB에도 따로 있음) |
| DB uid 14944 | 2022 | Paik S., Min, S.-K., Son, S.-W., An, S.… | How volcanic eruption latitudes diversify surface climate r… | 10.5194/acp-2022-187 | 제외 | ACP 토론 원고(preprint). Crossref에 최종 논문 연결 없음 |
| DB uid 14946 | 2022 | Paik S., Min S.-K., Son, S.-W., An, S.-… | Diverse Arctic Oscillation responses after volcanic eruptio… | 10.5194/egusphere-egu22-10958 | 제외 | EGU 2022 학회 초록 |
| DB uid 14947 | 2022 | Choi, Y.-J., Kim, S.-Y., Son, S.-W., An… | Super recovery of the Hadley Cell edge to the CO2 removal | 10.5194/egusphere-egu22-10935 | 제외 | EGU 2022 학회 초록 |

### B-3. 우리 목록에만 있는 항목 (51편, 지우지 않음)

51편 모두 Crossref 저자 목록에 `Jong-Seong Kug`(또는 `J.-S. Kug`)가 있다 → 오귀속 확실 0편.

| 분류 | 편수 | 판단 |
|---|---|---|
| 백업 공백 구간(2024-05 ~ 2025-08 출판) | 35 | 원본 사이트 No.263–297(35편)이 백업에 없다(캐시는 1쪽 20편, DB는 2024-04까지). 시기·편수가 정확히 맞아 원본에 있던 논문으로 추정, 확인 불가 |
| 캐시 시점 이후(2026-09 ~ 10 출판) | 6 | 캐시(2026-10) 첫 쪽에 없음. 원본 등록 전 출판으로 추정 |
| 원본 누락 추정 | 8 | 2021–2022 공저 5편 + 국내 학술지 공저 3편. Kug 공저 확인됨 |
| 원본 표기 오류(실제로는 원본에 있음) | 1 | 아래 표 |
| 중복 DOI(숨김) | 1 | 아래 표 |

2023년 이전 10편:

| DOI | 연도 | 학술지 | 제목 | 판단 |
|---|---|---|---|---|
| [10.1175/bams-d-22-0149.1](https://doi.org/10.1175/bams-d-22-0149.1) | 2022 | Bulletin of the American Mete… | Human Contribution to 2020/21-like Persistent Iran Meteorol… | 원본 누락 추정(공저, Crossref Kug 확인) |
| [10.1029/2021gl095516](https://doi.org/10.1029/2021gl095516) | 2021 | Geophysical Research Letters | Pacific Warming Pattern Diversity Modulated by Indo‐Pacific… | 원본 누락 추정(공저, Crossref Kug 확인) |
| [10.1175/jcli-d-21-0025.1](https://doi.org/10.1175/jcli-d-21-0025.1) | 2021 | Journal of Climate | Role of cloud feedback in continental warming response to C… | 원본 누락 추정(공저, Crossref Kug 확인) |
| [10.1175/mwr-d-21-0051.1](https://doi.org/10.1175/mwr-d-21-0051.1) | 2021 | Monthly Weather Review | Record-breaking summer rainfall in South Korea in 2020: Syn… | 원본 누락 추정(공저, Crossref Kug 확인) |
| [10.1007/s00382-021-05702-2](https://doi.org/10.1007/s00382-021-05702-2) | 2021 | Climate Dynamics | The influence of atmospheric intraseasonal oscillations on … | 원본 누락 추정(공저, Crossref Kug 확인) |
| [10.14191/atmos.2016.26.2.337](https://doi.org/10.14191/atmos.2016.26.2.337) | 2016 | Atmosphere | Assessment of Climate Variability over East Asia-Korea for … | 원본 누락 추정(국내 학술지 「대기」, 공저) |
| [10.15531/ksccr.2015.6.4.389](https://doi.org/10.15531/ksccr.2015.6.4.389) | 2015 | Journal of Climate Change Res… | Future Changes in Atmosphere Teleconnection over East Asia … | 원본 누락 추정(국내 학술지 「한국기후변화학회지」, 공저) |
| [10.1175/bams-eee_2014_ch20.1](https://doi.org/10.1175/bams-eee_2014_ch20.1) | 2015 | Bulletin of the American Mete… | Human Contribution to the 2014 Record High Sea Surface Temp… | 중복 DOI: 같은 논문을 원본은 10.1175/bams-d-15-00055.1(DB uid 14869)로 표시 → `hidden: true` + `note` |
| [10.14191/atmos.2014.24.1.089](https://doi.org/10.14191/atmos.2014.24.1.089) | 2014 | Atmosphere | Relation between Climate Variability in Korea and Two Types… | 원본 누락 추정(국내 학술지 「대기」, 공저) |
| [10.1007/s00382-007-0310-5](https://doi.org/10.1007/s00382-007-0310-5) | 2008 | Climate Dynamics | How accurately do coupled climate models predict the leadin… | 원본 표기 오류: 원본 DB uid 14760이 이 논문 DOI를 오타(`s00382-0070310-5`)로 달고 제목은 다른 논문(Current Status of ENSO Prediction Skill…, uid 14766과 중복)을 적었다 → 원본에 있던 논문으로 본다 |

<details><summary>백업 공백 구간 35편 · 캐시 이후 6편</summary>

| DOI | date | 학술지 | 제목 | 분류 |
|---|---|---|---|---|
| 10.1088/1748-9326/aeba9f | 2026-10-28 | Environmental Research Letters | Victoria mode drives the strengthening of tropical Atlantic… | 캐시 이후 |
| 10.1038/s41561-026-02125-8 | 2026-10-12 | Nature Geoscience | An abrupt shift towards a hotter and drier climate regime i… | 캐시 이후 |
| 10.1038/s43247-026-04018-5 | 2026-10-02 | Communications Earth & Enviro… | North Atlantic chlorophyll blooms modulate European hydrocl… | 캐시 이후 |
| 10.5194/esd-17-1381-2026 | 2026-09-28 | Earth System Dynamics | Regional contrasts of ecosystem productivity sensitivity to… | 캐시 이후 |
| 10.1088/1748-9326/aea34e | 2026-09-28 | Environmental Research Letters | Incomplete recovery in compound extreme events under a CO2 … | 캐시 이후 |
| 10.1126/sciadv.aee9228 | 2026-09-04 | Science Advances | Enhanced carbon loss in the Southern Ocean under mitigation… | 캐시 이후 |
| 10.1080/17538947.2025.2487058 | 2025-08-25 | International Journal of Digi… | Evaluation and prediction of the effects of planetary orbit… | 공백 구간 |
| 10.1175/jcli-d-24-0544.1 | 2025-08-15 | Journal of Climate | Contribution of Intraseasonal Variability to Uncertainty in… | 공백 구간 |
| 10.1126/sciadv.adv0282 | 2025-08-15 | Science Advances | Excess water availability in northern mid-high latitudes co… | 공백 구간 |
| 10.1175/jcli-d-24-0604.1 | 2025-08 | Journal of Climate | Mechanisms behind Seasonal Differences in the Recent Interd… | 공백 구간 |
| 10.5194/bg-22-3165-2025 | 2025-07-03 | Biogeosciences | Phytoplankton blooming mechanisms over the East China Sea d… | 공백 구간 |
| 10.1073/pnas.2426048122 | 2025-06-24 | Proceedings of the National A… | Abrupt shift of El Niño periodicity under CO2 mitigation | 공백 구간 |
| 10.1038/s41612-025-01087-9 | 2025-06-04 | npj Climate and Atmospheric S… | Asymmetric response of the Western North Pacific tropical c… | 공백 구간 |
| 10.1029/2024ef005787 | 2025-05 | Earth's Future | Irreversible Land Water Availability Changes From a Potenti… | 공백 구간 |
| 10.1038/s41612-025-01053-5 | 2025-04-27 | npj Climate and Atmospheric S… | A low-dimensional recursive deep learning model for El Niño… | 공백 구간 |
| 10.1038/s41467-025-57724-7 | 2025-04-03 | Nature Communications | Emergence of an oceanic CO2 uptake hole under global warming | 공백 구간 |
| 10.1088/1748-9326/adc28e | 2025-04-01 | Environmental Research Letters | Variability of upper troposphere–lower stratosphere ozone o… | 공백 구간 |
| 10.1016/j.jenvman.2025.125097 | 2025-04 | Journal of Environmental Mana… | Land use change-induced abrupt changes in vegetation and th… | 공백 구간 |
| 10.1029/2024rg000843 | 2025-03 | Reviews of Geophysics | The El Niño Southern Oscillation (ENSO) Recharge Oscillator… | 공백 구간 |
| 10.1126/sciadv.adn8819 | 2025-02-14 | Science Advances | Continued permafrost ecosystem carbon loss under net-zero a… | 공백 구간 |
| 10.1088/1748-9326/ad7b5c | 2024-12-01 | Environmental Research Letters | Asymmetric ENSO teleconnections in a symmetric CO2 concentr… | 공백 구간 |
| 10.1038/s41467-024-54339-2 | 2024-11-19 | Nature Communications | Pervasive fire danger continued under a negative emission s… | 공백 구간 |
| 10.1038/s43247-024-01870-1 | 2024-11-11 | Communications Earth & Enviro… | On the spatial double peak of the 2023–2024 El Niño event | 공백 구간 |
| 10.1038/s43247-024-01835-4 | 2024-11-03 | Communications Earth & Enviro… | Fast recovery of North Atlantic sea level in response to at… | 공백 구간 |
| 10.1038/s41612-024-00806-y | 2024-10-21 | npj Climate and Atmospheric S… | Synchronous decadal climate variability in the tropical Cen… | 공백 구간 |
| 10.1038/s41612-024-00799-8 | 2024-10-16 | npj Climate and Atmospheric S… | Data-driven investigation on the boreal summer MJO predicta… | 공백 구간 |
| 10.1038/s41612-024-00790-3 | 2024-10-07 | npj Climate and Atmospheric S… | Significant winter Atlantic Niño effect on ENSO and its fut… | 공백 구간 |
| 10.1088/2515-7620/ad8058 | 2024-10-01 | Environmental Research Commun… | Delayed ENSO impact on phytoplankton variability over the W… | 공백 구간 |
| 10.1038/s41467-024-50663-9 | 2024-07-23 | Nature Communications | Deep ocean warming-induced El Niño changes | 공백 구간 |
| 10.1088/1748-9326/ad5573 | 2024-07-01 | Environmental Research Letters | Precipitation-induced abrupt decrease of Siberian wildfire … | 공백 구간 |
| 10.1088/1748-9326/ad52ad | 2024-07-01 | Environmental Research Letters | Hysteresis of European summer precipitation under a symmetr… | 공백 구간 |
| 10.1029/2023gl107749 | 2024-06-28 | Geophysical Research Letters | Distinct Modulations of Northwest Pacific Tropical Cyclone … | 공백 구간 |
| 10.1038/s41586-024-07534-6 | 2024-06-27 | Nature | Explainable El Niño predictability from climate mode intera… | 공백 구간 |
| 10.1088/1748-9326/ad4db8 | 2024-06-01 | Environmental Research Letters | Intensified surface chlorophyll responses to the Indian Oce… | 공백 구간 |
| 10.1038/s41612-024-00674-6 | 2024-06-01 | npj Climate and Atmospheric S… | Fast reduction of Atlantic SST threatens Europe-wide gross … | 공백 구간 |
| 10.1029/2023ef004223 | 2024-06 | Earth's Future | How Does Plant CO2 Physiological Forcing Amplify Amazon War… | 공백 구간 |
| 10.1038/s41612-024-00660-y | 2024-05-23 | npj Climate and Atmospheric S… | Basin-dependent response of Northern Hemisphere winter bloc… | 공백 구간 |
| 10.1029/2024gl108272 | 2024-05-16 | Geophysical Research Letters | Fast and Slow Responses of Atlantic Meridional Overturning … | 공백 구간 |
| 10.1175/bams-d-23-0241.1 | 2024-05 | Bulletin of the American Mete… | Climate Models Indicate Compensating Effects between Anthro… | 공백 구간 |
| 10.1038/s41558-024-01976-6 | 2024-05 | Nature Climate Change | Western North Pacific tropical cyclone activity modulated b… | 공백 구간 |
| 10.1038/s41558-024-01971-x | 2024-05 | Nature Climate Change | Asymmetric hysteresis response of mid-latitude storm tracks… | 공백 구간 |

</details>

### B-4. 원본 자료의 DOI·중복 오류 (제목 기준으로 맞춤, 우리 목록은 고치지 않음)

| 원본 | 원본 연도 | 원본 제목 | 원본 링크/DOI | 맞춘 우리 DOI | 유형 |
|---|---|---|---|---|---|
| DB uid 14746 | 2004 | A Near-Annual Pacific Ocean Basin Mode. J. Climate, 17,2478… | `http://dx.doi.org/10.1175/1520-0442(2004)017%3C2478:AN…` | 10.1175/1520-0442(2004)017<2478:anpobm>2.0.co;2 | URL 인코딩(실질 일치) |
| DB uid 14751 | 2006 | Interactive feedback between ENSO and the Indian Ocean. J. … | `https://journals.ametsoc.org/search?f_0=author&amp;q_0…` | 10.1175/jcli3660.1 | DOI 아닌 링크 |
| DB uid 14755 | 2007 | The influence of ENSO on the generation of decadal variabil… | `http://web.yonsei.ac.kr/climate/board/4/20070817184920…` | 10.1175/jcli4017.1 | DOI 아닌 링크 |
| DB uid 14760 | 2008 | Current Status of ENSO Prediction Skill in Coupled Ocean-At… | `http://dx.doi.org/10.1007/s00382-0070310-5` | 10.1007/s00382-008-0397-3 | DOI 오타(실제 10.1007/s00382-007-0310-5 "How accurately…"), 제목은 uid 14766과 중복 |
| DB uid 14763 | 2008 | Optimal multi-model ensemble method in seasonal climate pre… | `https://hdl.handle.net/10371/20243` | (DOI 없음) | DOI 아닌 링크 |
| DB uid 14812 | 2012 | Revisited relationship between tropical and North Pacific s… | `http://dx.doi.org/10.10269/2011GL050005` | 10.1029/2011gl050005 | DOI 오타 |
| DB uid 14825 | 2012 | Improved simulation of two types of El Nino in CMIP5 models… | `http://dx.doi.org/10.1088/1748-9326/7/3/039502` | 10.1088/1748-9326/7/3/034002 | 정오표(Corrigendum) DOI |
| DB uid 14854 | 2015 | Intra-winter atmospheric circulation changes over East Asia… | `http://dx.doi.org/10.1007/s13143-000-0000-0` | 10.1007/s13143-014-0059-9 | 자리표시 DOI |
| DB uid 14859 | 2015 | Amplified Arctic warming by phytoplankton under greenhouse … | `http://dx.doi.org/10.1073/pnas.1416884112/-/DCSuppleme…` | 10.1073/pnas.1416884112 | 부록 링크(DOI 뒤 /-/DCSupplemental) |
| DB uid 14863 | 2016 | Precipitation variability in September over the Korean Peni… | `http://dx.doi.org/10.1038/NCLIMATE2743` | 10.1007/s00382-015-2776-x | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14864 | 2015 | ENSO and greenhouse warming. | `http://dx.doi.org/10.1007/s00382-015-2776-x` | 10.1038/nclimate2743 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14871 | 2016 | Impact of Two Distinct Teleconnection Patterns Induced by W… | `http://dx.doi.org/10.1175/JCLI-D-14-00790.1` | 10.1175/jcli-d-15-0406.1 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14872 | 2015 | Temperature Variation over East Asia during the Lifecycle o… | `http://dx.doi.org/10.1175/JCLI-D-15-0406.1` | 10.1175/jcli-d-14-00790.1 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14877 | 2017 | How well do climate models simulate atmospheric teleconncti… | `http://dx.doi.org/100.1007/s00382-016-3121-8` | 10.1007/s00382-016-3121-8 | DOI 오타(100.1007) |
| DB uid 14883 | 2018 | Relative roles of equatorial central Pacific and western No… | `http://dx.doi.org/10.1038/ngeo2986` | 10.1007/s00382-017-3779-6 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14884 | 2017 | Reduced North American terrestrial primary productivity lin… | `http://dx.doi.org/10.1007/s00382-017-3779-6` | 10.1038/ngeo2986 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14886 | 2017 | Intensification of terrestrial carbon cycle related to El N… | `http://dx.doi.org/10.1007/s00382-017-4036-8` | 10.1038/s41467-017-01831-7 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14887 | 2018 | Impact of chlorophyll bias on the tropical Pacific mean cli… | `http://dx.doi.org/10.1038/s41467-017-01831-7` | 10.1007/s00382-017-4036-8 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14894 | 2018 | El Niño–Southern Oscillation complexity, Nature, 559, 535-5… | `http://dx.doi.org/10.1029/2018JD028935` | 10.1038/s41586-018-0252-6 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14895 | 2018 | What controls ENSO teleconnection to East Asia? Role of wes… | `http://dx.doi.org/10.1038/s41586-018-0252-6` | 10.1029/2018jd028935 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14899 | 2019 | Pantropical climate interactions, Science, 363 | `http://dx.doi.org/10.1007/s00382-019-04765-6` | 10.1126/science.aav4236 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14900 | 2019 | "How well do current climate models simulate the linkage be… | `http://dx.doi.org/10.1126/science.aav4236` | 10.1007/s00382-019-04765-6 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14902 | 2019 | The role of oscillating Southern Hemisphere westerly winds:… | `http://dx.doi.org/10.1029/2019GL085943` | 10.1175/jcli-d-19-0364.1 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14903 | 2019 | Role of local air-sea interaction in fire activity over Equ… | `http://dx.doi.org/10.1175/JCLI-D-19-0364.1` | 10.1029/2019gl085943 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14904 | 2020 | Extensive fires in southeastern Siberian permafrost linked … | `http://dx.doi.org/10.1007/s00382-019-04901-2` | 10.1126/sciadv.aax3308 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14905 | 2019 | How does ENSO diversity limit the skill of tropical Pacific… | `http://dx.doi.org/10.1126/sciadv.aax3308` | 10.1007/s00382-019-04901-2 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14911 | 2019 | Biogeophysical feedback of phytoplankton on the Arctic clim… | `http://dx.doi.org/10.1038/s41586-019-0994-9` | 10.1007/s00382-018-4450-6 | 다른 논문의 DOI(정오표 DOI) |
| DB uid 14915 | 2020 | Two a﻿spects of Decadal ENSO Variability Modulating the Lon… | `http://dx.doi.org/10.1038/s41467-020-15924-3` | 10.1029/2019gl086390 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14916 | 2020 | The intensification of Arctic warming as a result of CO2 ph… | `http://dx.doi.org/10.1029/2019GL086390` | 10.1038/s41467-020-15924-3 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14918 | 2020 | Mid-latitude leading double-dip La Niña., International Jou… | `http://dx.doi.org/10.1002/essoar.10503236.1` | 10.1002/joc.6772 | 인접 항목(Zhao 2020 GRL)의 preprint DOI |
| DB uid 14919 | 2020 | Diversity of Pacific Meridional Mode and its distinct impac… | `http://dx.doi.org/10.1002/joc.6772` | 10.1029/2020gl088993 | 다른 논문의 DOI(인접 항목과 뒤바뀜) |
| DB uid 14929 | 2021 | Zonally asymmetric phytoplankton response to the Southern A… | `https://www.nature.com/articles/s41598-021-89720-4` | 10.1038/s41598-021-89720-4 | DOI 아닌 링크 |

유형별: URL 인코딩(실질 일치) 1, DOI 아닌 링크 4, DOI 오타(실제 10.1007/s00382-007-0310-5 "How accurately…"), 제목은 uid 14766과 중복 1, DOI 오타 1, 정오표(Corrigendum) DOI 1, 자리표시 DOI 1, 부록 링크(DOI 뒤 /-/DCSupplemental) 1, 다른 논문의 DOI(인접 항목과 뒤바뀜) 19, DOI 오타(100.1007) 1, 다른 논문의 DOI(정오표 DOI) 1, 인접 항목(Zhao 2020 GRL)의 preprint DOI 1

원본 DB 안의 중복(같은 논문이 두 번 등록) 7쌍:

| 우리 DOI | 원본 항목 | 비고 |
|---|---|---|
| 10.1007/s00382-008-0397-3 | DB uid 14760, DB uid 14766 |  |
| 10.1007/s00382-012-1640-5 | DB uid 14842, DB uid 14907 | 연도 다르게 두 번(2012/2014) |
| 10.1175/jcli-d-20-0691.1 | DB uid 14922, DB uid 14927 |  |
| 10.1126/sciadv.adg1801 | DB uid 14987, DB uid 14993 |  |
| 10.1126/sciadv.adh8442 | DB uid 14988, DB uid 14995 |  |
| 10.1038/s41612-023-00448-6 | DB uid 14989, DB uid 14994 |  |
| 10.1029/2023gl105864 | DB uid 14991, DB uid 14998 | 연도 다르게 두 번(2023/2024) |

### B-5. 원본 연도 ≠ 우리 연도 (고치지 않음)

우리 연도는 `pubtools.pub_date` 규칙(published-print 우선). 원본은 대부분 온라인 선공개 연도를 적었다.

| DOI | 원본 | 원본 연도 | 우리 연도 | 우리 date | 학술지 | 제목 |
|---|---|---|---|---|---|---|
| 10.1007/s00382-008-0483-6 | DB uid 14774 | 2008 | 2009 | 2009-09 | Climate Dynamics | Effects of the low-frequency zonal wind variation on the hi… |
| 10.1007/s00382-009-0606-8 | DB uid 14793 | 2009 | 2010 | 2010-11 | Climate Dynamics | A general rule for synoptic-eddy feedback onto low-frequenc… |
| 10.1007/s00382-010-0873-4 | DB uid 14801 | 2010 | 2011 | 2011-08 | Climate Dynamics | Impact of transient eddies on extratropical seasonal-mean p… |
| 10.1007/s00382-011-1142-x | DB uid 14813 | 2011 | 2012 | 2012-04 | Climate Dynamics | Greening in the circumpolar high-latitude may amplify warmi… |
| 10.1002/joc.2329 | DB uid 14815 | 2011 | 2012 | 2012-06-15 | International Journal of Clim… | Eastward shift of the Pacific/North American pattern on an … |
| 10.1007/s00382-012-1640-5 | DB uid 14842 | 2012 | 2014 | 2014-01 | Climate Dynamics | Marine biological feedback associated with Indian Ocean Dip… |
| 10.1007/s13143-019-00146-5 | DB uid 14901 | 2019 | 2020 | 2020-08 | Asia-Pacific Journal of Atmos… | Impacts of SST Pattern Represented by Ocean Temperature nea… |
| 10.1175/jcli-d-19-0364.1 | DB uid 14902 | 2019 | 2020 | 2020-03-15 | Journal of Climate | The Role of Oscillating Southern Hemisphere Westerly Winds:… |
| 10.1002/joc.6772 | DB uid 14918 | 2020 | 2021 | 2021-01 | International Journal of Clim… | Mid‐latitude leading double‐dip La Niña |
| 10.1007/s00382-023-06918-0 | DB uid 14972 | 2023 | 2024 | 2024-01 | Climate Dynamics | Intermodel relation between present-day warm pool intensity… |
| 10.1029/2023gl105864 | DB uid 14991 | 2023 | 2024 | 2024-01-16 | Geophysical Research Letters | Mutating ENSO Impact on Northwest Pacific Tropical Cyclones… |
| 10.1029/2023ef003709 | DB uid 14992 | 2023 | 2024 | 2024-01 | Earth's Future | Role of Atlantification in Enhanced Primary Productivity in… |

### B-6. 교신저자 표기 (원본 근거별)

- 캐시(2026-10) 첫 쪽 20편 중 별표가 있는 19편: `J.-S. Kug*` 16편 → `corresponding: true`; 별표 저자 전원을 `corr_authors`로(19편). No.298(Lee, Kim, Kug 2025 jhl)은 별표 없음.
- DB(2024-04) 제목 끝 `(CA)` 표기 37편(우리 연도 2009–2016년 논문): 교수님 교신저자 표기 → `corresponding: true` + `corr_authors: ["Kug, J.-S."]`.
- 별표 저자 이름은 모두 우리 authors 표기와 1:1로 맞았다(미매칭 0, 모호 0).
- 기존 `corresponding: true` 5편(수동 지정, 원본에 별표·CA 근거 없음)은 그대로 둠. 결과: corresponding 58편, corr_authors 56편.
- DB uid 14875 이후 등록분(2016년~2024-04 논문)과 공백 구간 35편은 원본에 교신저자 표시가 없어 손대지 않았다.

<details><summary>교신저자 표기 목록</summary>

| 원본 | 근거 | DOI | 연도 | corr_authors | corresponding |
|---|---|---|---|---|---|
| 캐시 No.317 | * | 10.1088/1748-9326/ae84ec | 2026 | Kim, S., Kug, J.-S. | true |
| 캐시 No.316 | * | 10.1029/2026ef008209 | 2026 | Kug, J.-S. | true |
| 캐시 No.315 | * | 10.1038/s41467-026-74381-6 | 2026 | Iwakiri, T., Kug, J.-S. | true |
| 캐시 No.314 | * | 10.1038/s41467-026-73838-y | 2026 | Iwakiri, T., Kug, J.-S. | true |
| 캐시 No.313 | * | 10.1007/s00382-026-08202-3 | 2026 | Yeh, S.-W. | - |
| 캐시 No.312 | * | 10.1126/sciadv.aeb2316 | 2026 | Zhan, R., Liu, Y. | - |
| 캐시 No.311 | * | 10.1029/2025ef007636 | 2026 | Kug, J.-S. | true |
| 캐시 No.310 | * | 10.1038/s41467-026-72898-4 | 2026 | Kug, J.-S. | true |
| 캐시 No.309 | * | 10.1038/s43247-026-03548-2 | 2026 | Min, S.-K. | - |
| 캐시 No.308 | * | 10.1038/s41467-026-70945-8 | 2026 | Kug, J.-S. | true |
| 캐시 No.307 | * | 10.1038/s41467-026-70140-9 | 2026 | Kim, G.-I., Kug, J.-S. | true |
| 캐시 No.306 | * | 10.1038/s41612-026-01355-2 | 2026 | An, S.-I., Kug, J.-S. | true |
| 캐시 No.305 | * | 10.1016/j.jenvman.2025.128446 | 2026 | Kug, J.-S. | true |
| 캐시 No.304 | * | 10.1038/s41467-025-66494-1 | 2025 | Kug, J.-S. | true |
| 캐시 No.303 | * | 10.1038/s41467-025-66143-7 | 2025 | Geng, X., Kug, J.-S. | true |
| 캐시 No.302 | * | 10.5194/esd-16-2101-2025 | 2025 | Kug, J.-S. | true |
| 캐시 No.301 | * | 10.1038/s41612-025-01220-8 | 2025 | Park, J.-H., Koo, J.-H., Kug, J.-S. | true |
| 캐시 No.300 | * | 10.1175/jcli-d-24-0437.1 | 2025 | Kug, J.-S. | true |
| 캐시 No.299 | * | 10.1038/s43247-025-02742-y | 2025 | Kug, J.-S. | true |
| DB uid 14772 | CA | 10.1007/s00704-008-0067-8 | 2009 | Kug, J.-S. | true |
| DB uid 14774 | CA | 10.1007/s00382-008-0483-6 | 2009 | Kug, J.-S. | true |
| DB uid 14777 | CA | 10.1007/s00382-009-0582-z | 2009 | Kug, J.-S. | true |
| DB uid 14783 | CA | 10.1007/s00382-009-0586-8 | 2010 | Kug, J.-S. | true |
| DB uid 14785 | CA | 10.1029/2009jd012813 | 2010 | Kug, J.-S. | true |
| DB uid 14791 | CA | 10.1029/2010jd014160 | 2010 | Kug, J.-S. | true |
| DB uid 14801 | CA | 10.1007/s00382-010-0873-4 | 2011 | Kug, J.-S. | true |
| DB uid 14809 | CA | 10.1029/2011jd016526 | 2011 | Kug, J.-S. | true |
| DB uid 14813 | CA | 10.1007/s00382-011-1142-x | 2012 | Kug, J.-S. | true |
| DB uid 14814 | CA | 10.4217/opr.2012.34.1.029 | 2012 | Kug, J.-S. | true |
| DB uid 14815 | CA | 10.1002/joc.2329 | 2012 | Kug, J.-S. | true |
| DB uid 14817 | CA | 10.1007/s00382-011-1157-3 | 2012 | Kug, J.-S. | true |
| DB uid 14819 | CA | 10.1175/jcli-d-11-00303.1 | 2012 | Kug, J.-S. | true |
| DB uid 14822 | CA | 10.1016/j.pocean.2012.04.005 | 2012 | Kug, J.-S. | true |
| DB uid 14823 | CA | 10.1029/2012jd018090 | 2012 | Kug, J.-S. | true |
| DB uid 14827 | CA | 10.1038/ngeo1686 | 2013 | Kug, J.-S. | true |
| DB uid 14830 | CA | 10.1007/s13143-013-0020-3 | 2013 | Kug, J.-S. | true |
| DB uid 14831 | CA | 10.14191/atmos.2013.23.1.063 | 2013 | Kug, J.-S. | true |
| DB uid 14833 | CA | 10.1038/nclimate1785 | 2013 | Kug, J.-S. | true |
| DB uid 14835 | CA | 10.1002/grl.50729 | 2013 | Kug, J.-S. | true |
| DB uid 14836 | CA | 10.1016/j.pocean.2013.07.005 | 2013 | Kug, J.-S. | true |
| DB uid 14842 | CA | 10.1007/s00382-012-1640-5 | 2014 | Kug, J.-S. | true |
| DB uid 14845 | CA | 10.1016/j.pocean.2014.03.013 | 2014 | Kug, J.-S. | true |
| DB uid 14846 | CA | 10.1007/s13143-014-0013-x | 2014 | Kug, J.-S. | true |
| DB uid 14847 | CA | 10.1007/s00382-013-2008-1 | 2014 | Kug, J.-S. | true |
| DB uid 14849 | CA | 10.1007/s00382-013-2009-0 | 2014 | Kug, J.-S. | true |
| DB uid 14851 | CA | 10.1007/s00382-014-2064-1 | 2014 | Kug, J.-S. | true |
| DB uid 14853 | CA | 10.1007/s00382-014-2349-4 | 2015 | Kug, J.-S. | true |
| DB uid 14854 | CA | 10.1007/s13143-014-0059-9 | 2015 | Kug, J.-S. | true |
| DB uid 14856 | CA | 10.1007/s00382-015-2551-z | 2015 | Kug, J.-S. | true |
| DB uid 14857 | CA | 10.1175/jcli-d-14-00376.1 | 2015 | Kug, J.-S. | true |
| DB uid 14859 | CA | 10.1073/pnas.1416884112 | 2015 | Kug, J.-S. | true |
| DB uid 14860 | CA | 10.1007/s13143-015-0066-5 | 2015 | Kug, J.-S. | true |
| DB uid 14863 | CA | 10.1007/s00382-015-2776-x | 2016 | Kug, J.-S. | true |
| DB uid 14870 | CA | 10.1175/jcli-d-14-00721.1 | 2015 | Kug, J.-S. | true |
| DB uid 14872 | CA | 10.1175/jcli-d-14-00790.1 | 2015 | Kug, J.-S. | true |
| DB uid 14874 | CA | 10.1007/s00382-012-1420-2 | 2013 | Kug, J.-S. | true |

</details>

### B-7. 1차 보고서 확인 필요 항목 ↔ 원본

| 1차 항목 | 원본 | 처리 |
|---|---|---|
| OpenAlex의 DOI 없는 국내 학술지 후보 13건(10-1절) | W1916742489(Kug & An 2010)만 원본 DB uid 14790에 있음. 나머지 12건(2001–2003 「대기」 9건, 2015 MJO·모델 편향 2건, 2020 GRL 일본어 기계번역 1건)은 원본에 없음 | 1건 직접 입력(`source: backup`, `url`, `note`), 12건 미추가 |
| APJAS 2008 "Optimal multi-model…"의 `Kang, I.-K.` | DB uid 14763: `Kang, I.-S.`, Asia-Pacific J. Atmos. Sci., 44, 259-267, 링크 `hdl.handle.net/10371/20243` | `Kang, I.-S.`로 정정, `url` 추가(권·쪽은 원본과 일치) |
| 숨긴 BAMS DOI 10.1175/bams-eee_2014_ch20.1 | 원본 DB uid 14869는 같은 논문을 10.1175/bams-d-15-00055.1(이미 표시 중)로 표시 | 중복이므로 `needs_review` → `hidden: true` + `note` |
| ORCID DOI 오기(jcli-d-11-00696.1 → jcli-d-12-00078.1) | DB uid 14821 "Indian Ocean feedback to the ENSO transition in a multimodel ensemble" = 10.1175/JCLI-D-12-00078.1. jcli-d-11-00696.1은 원본에 없음 | 1차 정정이 맞음(변경 없음). 교수님 ORCID 수정은 여전히 필요 |

### B-8. 사람이 확인할 점

1. **백업 공백 35편**(원본 No.263–297): 백업에 원본이 없어 대조하지 못했다. 우리 목록의 2024-05 ~ 2025-08 출판 35편과 시기·편수가 정확히 맞지만 1:1 확인은 아니다. 원본 DB 최신 덤프(2024-04 이후)나 관리자 화면 목록이 있으면 다시 대조한다.
2. **교신저자 근거가 없는 구간**: 원본에 표시가 없는 2016년 ~ 2024-04 등록분, 공백 35편, 2026-09 이후 6편은 `corresponding`을 넣지 않았다. 필요하면 교수님·학생이 확인해 `corresponding`/`corr_authors`를 넣는다.
3. **`(CA)` 해석**: DB 제목 끝 `(CA)`를 "교수님이 교신저자"로 보고 37편에 `corresponding: true` + `corr_authors: ["Kug, J.-S."]`를 넣었다. 이 중 20편은 Kug가 마지막 저자가 아니다(예: Min et al. 2015 APJAS 리뷰 10.1007/s13143-015-0066-5는 12명 중 4번째). 대표 몇 편만 원문 교신저자 표시로 확인 권장.
4. **원본 누락 추정 8편**(B-3: 2021–2022 공저 5편, 국내 학술지 공저 3편): 지우지 않고 표시 유지. 원본에 없던 이유(의도적 제외인지)는 교수님 확인.
5. **새로 넣은 「대기」 2010 논문**: 원본은 연도·권·쪽만 있고, 호(2)·발행월(2010-06)은 OpenAlex 값이다. 학술지명은 Crossref의 다른 「대기」 논문과 같게 `Atmosphere`로 적었다.
6. **수집 스크립트 재실행 주의(주 세션 담당 `scripts/`)**: `fetch_publications.py`의 `MANUAL_FIELDS`는 `corresponding, featured, image, links, hidden`뿐이라, 다시 돌리면 이번에 넣은 `corr_authors`(56편)·`note`·`url`·`source`가 사라지고, DOI 없는 ORCID 항목(APJAS 2008)은 ORCID 메타데이터로 다시 만들어져 `Kang, I.-K.`로 돌아간다. `MANUAL_FIELDS`에 `corr_authors, note, url, source`를 더하거나, 재실행 뒤 이 대조를 다시 적용해야 한다. (`corresponding`·`hidden`은 보존된다. `source: backup` 항목은 "출처에서 못 찾은 기존 항목"으로 그대로 남는다.)
7. 원본 사이트 자체 오류(B-4: DOI가 인접 논문과 뒤바뀐 19행, 오타·자리표시 DOI, 중복 7쌍)는 우리 목록에 영향이 없다(제목 기준으로 맞췄고, 우리 DOI는 Crossref 기준). 새 사이트로 옮기면 함께 해소된다.

### B-9. 작업 기록

- 파싱·대조 스크립트(스크래치, `python -I`, 백업 경로를 인자로 전달): `parse_cache.py`(캐시 HTML 행 추출), `orig.py`(캐시 20행 + DB 262행 정리, 저자 `*` 분리), `recon.py`(DOI/제목 매칭), `apply.py`(yaml 반영, `pubtools.save_pubs` 사용), `gen_md.py`(이 절의 표). 위치: `/tmp/claude-1500/-data5-CSL-homepage/3efc62de-b047-4116-9c2c-f3e7d402120c/scratchpad/`.
- Crossref 조회는 `.cache/pubs/`(fetch_publications.py와 같은 키 규칙) 캐시를 썼다. 캐시에 없던 것(원본만 항목 DOI·제목 검색 등)만 새로 요청했고, OpenAlex는 W1916742489 1건을 조회했다.
- 바꾼 파일: `data/publications.yaml`(교신저자 56편, BAMS 숨김 1, APJAS 2008 저자·url, 추가 1, meta), 이 보고서. 다른 파일은 건드리지 않았다.

