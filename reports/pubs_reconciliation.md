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
