
# -*- coding: utf-8 -*-
# 注入模块5：多语言 i18n key（四大新模块）

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== ZH 中文追加 =====
ZH_KEYS = """
    // 排行榜升级
    lb_tab_roi:'月收益排行', lb_tab_wr:'胜率排行', lb_tab_stable:'最稳排行', lb_tab_new:'新秀榜',
    // 交易广场
    nav_square:'交易广场', sq_title:'交易广场', sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频',
    sq_post_ph:'分享你的市场观点、交易逻辑、仓位分析...', sq_post_btn:'发布观点',
    sq_filter_all:'全部', sq_filter_bull:'看多', sq_filter_bear:'看空', sq_filter_hot:'热门',
    sq_pair_label:'交易对', sq_sentiment_label:'情绪',
    // 策略市场
    nav_stratmarket:'策略市场', sm_title:'策略市场', sm_subtitle:'发现、分享、一键复用顶级量化策略',
    sm_upload_title:'发布我的策略', sm_upload_btn:'上传策略', sm_filter_all:'全部',
    sm_filter_trend:'趋势跟踪', sm_filter_grid:'网格', sm_filter_quant:'量化', sm_filter_arb:'套利',
    sm_name_label:'策略名称', sm_asset_label:'适用品种', sm_price_label:'定价(USD/月,0=免费)',
    sm_code_label:'策略代码 (Pine Script/伪代码)', sm_submit_btn:'提交审核', sm_backtest:'回测',
    sm_copy:'复制', sm_subscribe:'订阅',
    // 信号广播
    nav_signals:'信号广播', sig_title:'信号广播', sig_subtitle:'实时交易信号，一键订阅推送，接入自动建仓',
    sig_publish_title:'发布交易信号', sig_tab_live:'实时信号', sig_tab_sources:'信号源', sig_tab_history:'历史记录',
    sig_pair:'交易对', sig_dir:'方向', sig_dir_buy:'做多', sig_dir_sell:'做空',
    sig_entry:'入场价', sig_sl:'止损', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'信号说明', sig_publish_btn:'广播信号',
    sig_follow:'跟单信号', sig_share:'分享', sig_subscribe_bc:'订阅信号源',"""

ZH_ANCHOR = "    ao_start:'启动自动建仓', ao_stop:'停止运行', ao_status_off:'● 未启动', ao_status_on:'🟢 运行中',"
if ZH_ANCHOR in content:
    content = content.replace(ZH_ANCHOR, ZH_KEYS + '\n    ' + ZH_ANCHOR.strip(), 1)
    print('ZH i18n injected OK')
else:
    print('ZH ANCHOR NOT FOUND')

# ===== EN 英文追加 =====
EN_KEYS = """
    // Leaderboard upgrade
    lb_tab_roi:'Monthly ROI', lb_tab_wr:'Win Rate', lb_tab_stable:'Most Stable', lb_tab_new:'Rising Stars',
    // Trading Square
    nav_square:'Trading Square', sq_title:'Trading Square', sq_subtitle:'Share views, discover sentiment, sync with global traders',
    sq_post_ph:'Share your market view, trade logic, position analysis...', sq_post_btn:'Post',
    sq_filter_all:'All', sq_filter_bull:'Bullish', sq_filter_bear:'Bearish', sq_filter_hot:'Hot',
    sq_pair_label:'Pair', sq_sentiment_label:'Sentiment',
    // Strategy Market
    nav_stratmarket:'Strategy Market', sm_title:'Strategy Market', sm_subtitle:'Discover, share, and copy top quant strategies',
    sm_upload_title:'Publish My Strategy', sm_upload_btn:'Upload Strategy', sm_filter_all:'All',
    sm_filter_trend:'Trend', sm_filter_grid:'Grid', sm_filter_quant:'Quant', sm_filter_arb:'Arb',
    sm_name_label:'Strategy Name', sm_asset_label:'Asset', sm_price_label:'Price (USD/mo, 0=Free)',
    sm_code_label:'Strategy Code (Pine Script/Pseudocode)', sm_submit_btn:'Submit for Review', sm_backtest:'Backtest',
    sm_copy:'Copy', sm_subscribe:'Subscribe',
    // Signal Broadcast
    nav_signals:'Signal Broadcast', sig_title:'Signal Broadcast', sig_subtitle:'Live signals, one-click subscribe, connect to Auto Open',
    sig_publish_title:'Publish Trade Signal', sig_tab_live:'Live Signals', sig_tab_sources:'Signal Sources', sig_tab_history:'History',
    sig_pair:'Pair', sig_dir:'Direction', sig_dir_buy:'Buy', sig_dir_sell:'Sell',
    sig_entry:'Entry', sig_sl:'Stop Loss', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'Signal Note', sig_publish_btn:'Broadcast Signal',
    sig_follow:'Follow Signal', sig_share:'Share', sig_subscribe_bc:'Subscribe Source',"""

EN_ANCHOR = "    ao_start:'Start Auto Open', ao_stop:'Stop', ao_status_off:'● Stopped', ao_status_on:'🟢 Running',"
if EN_ANCHOR in content:
    content = content.replace(EN_ANCHOR, EN_KEYS + '\n    ' + EN_ANCHOR.strip(), 1)
    print('EN i18n injected OK')
else:
    print('EN ANCHOR NOT FOUND')

# ===== JA 日本語追加 =====
JA_KEYS = """
    // リーダーボード
    lb_tab_roi:'月利ランク', lb_tab_wr:'勝率ランク', lb_tab_stable:'安定ランク', lb_tab_new:'新星',
    // トレード広場
    nav_square:'トレード広場', sq_title:'トレード広場', sq_subtitle:'見解を共有し、世界のトレーダーとつながる',
    sq_post_ph:'相場見解・ポジション分析を共有...', sq_post_btn:'投稿',
    sq_filter_all:'すべて', sq_filter_bull:'強気', sq_filter_bear:'弱気', sq_filter_hot:'ホット',
    sq_pair_label:'銘柄', sq_sentiment_label:'センチメント',
    // ストラテジーマーケット
    nav_stratmarket:'ストラテジー市場', sm_title:'ストラテジー市場', sm_subtitle:'トップ戦略を発見・共有・コピー',
    sm_upload_title:'戦略を公開', sm_upload_btn:'戦略アップロード', sm_filter_all:'すべて',
    sm_filter_trend:'トレンド', sm_filter_grid:'グリッド', sm_filter_quant:'クオンツ', sm_filter_arb:'アーブ',
    sm_name_label:'戦略名', sm_asset_label:'銘柄', sm_price_label:'価格(USD/月, 0=無料)',
    sm_code_label:'戦略コード', sm_submit_btn:'審査に提出', sm_backtest:'バックテスト',
    sm_copy:'コピー', sm_subscribe:'購読',
    // シグナル放送
    nav_signals:'シグナル放送', sig_title:'シグナル放送', sig_subtitle:'リアルタイム信号・購読・自動建玉連携',
    sig_publish_title:'シグナル配信', sig_tab_live:'ライブ', sig_tab_sources:'配信元', sig_tab_history:'履歴',
    sig_pair:'銘柄', sig_dir:'方向', sig_dir_buy:'ロング', sig_dir_sell:'ショート',
    sig_entry:'エントリー', sig_sl:'SL', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'メモ', sig_publish_btn:'シグナル配信',
    sig_follow:'シグナルフォロー', sig_share:'共有', sig_subscribe_bc:'配信元を購読',"""

JA_ANCHOR = "    ao_start:'自動建玉開始', ao_stop:'停止', ao_status_off:'● 停止中', ao_status_on:'🟢 実行中',"
if JA_ANCHOR in content:
    content = content.replace(JA_ANCHOR, JA_KEYS + '\n    ' + JA_ANCHOR.strip(), 1)
    print('JA i18n injected OK')
else:
    print('JA ANCHOR NOT FOUND')

# ===== KO 한국어 추가 =====
KO_KEYS = """
    // 리더보드
    lb_tab_roi:'월 수익 순위', lb_tab_wr:'승률 순위', lb_tab_stable:'안정 순위', lb_tab_new:'신진',
    // 트레이딩 스퀘어
    nav_square:'트레이딩 스퀘어', sq_title:'트레이딩 스퀘어', sq_subtitle:'시각 공유, 감성 발견, 글로벌 트레이더와 연결',
    sq_post_ph:'시장 전망·포지션 분석을 공유하세요...', sq_post_btn:'게시',
    sq_filter_all:'전체', sq_filter_bull:'강세', sq_filter_bear:'약세', sq_filter_hot:'인기',
    sq_pair_label:'페어', sq_sentiment_label:'감성',
    // 전략 시장
    nav_stratmarket:'전략 시장', sm_title:'전략 시장', sm_subtitle:'최고 퀀트 전략 발견·공유·복사',
    sm_upload_title:'내 전략 공개', sm_upload_btn:'전략 업로드', sm_filter_all:'전체',
    sm_filter_trend:'트렌드', sm_filter_grid:'그리드', sm_filter_quant:'퀀트', sm_filter_arb:'차익',
    sm_name_label:'전략명', sm_asset_label:'종목', sm_price_label:'가격(USD/월, 0=무료)',
    sm_code_label:'전략 코드', sm_submit_btn:'심사 제출', sm_backtest:'백테스트',
    sm_copy:'복사', sm_subscribe:'구독',
    // 신호 방송
    nav_signals:'신호 방송', sig_title:'신호 방송', sig_subtitle:'실시간 신호·구독·자동 진입 연결',
    sig_publish_title:'신호 발행', sig_tab_live:'실시간', sig_tab_sources:'신호원', sig_tab_history:'히스토리',
    sig_pair:'페어', sig_dir:'방향', sig_dir_buy:'롱', sig_dir_sell:'숏',
    sig_entry:'진입', sig_sl:'손절', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'메모', sig_publish_btn:'신호 방송',
    sig_follow:'신호 팔로우', sig_share:'공유', sig_subscribe_bc:'신호원 구독',"""

KO_ANCHOR = "    ao_start:'자동 진입 시작', ao_stop:'정지', ao_status_off:'● 정지됨', ao_status_on:'🟢 실행 중',"
if KO_ANCHOR in content:
    content = content.replace(KO_ANCHOR, KO_KEYS + '\n    ' + KO_ANCHOR.strip(), 1)
    print('KO i18n injected OK')
else:
    print('KO ANCHOR NOT FOUND')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('All i18n injected. File size:', len(content))
