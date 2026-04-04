// QuantAI HarmonyOS NEXT - 主页面（TabBar 导航）
// ArkTS + ArkUI 声明式 UI

import router from '@ohos.router';
import { MarketPage } from './MarketPage';
import { AIAssistantPage } from './AIAssistantPage';
import { PositionsPage } from './PositionsPage';
import { AccountPage } from './AccountPage';

// 全局颜色常量（赛博暗色主题）
const COLOR_BG = '#0A1628';
const COLOR_CARD = '#111F35';
const COLOR_GREEN = '#00C896';
const COLOR_RED = '#FF4B6E';
const COLOR_TEXT = '#E8F4FF';
const COLOR_MUTED = '#6B8DB0';
const COLOR_BORDER = '#1E3050';

@Entry
@Component
struct Index {
  @State currentTab: number = 0;

  @Builder
  TabBarItem(icon: string, label: string, index: number) {
    Column() {
      Text(icon)
        .fontSize(22)
        .opacity(this.currentTab === index ? 1 : 0.5)
      Text(label)
        .fontSize(10)
        .fontColor(this.currentTab === index ? COLOR_GREEN : COLOR_MUTED)
        .margin({ top: 2 })
    }
    .width('100%')
    .height(56)
    .justifyContent(FlexAlign.Center)
    .onClick(() => { this.currentTab = index; })
  }

  build() {
    Column() {
      // 主内容区
      Stack() {
        if (this.currentTab === 0) {
          DashboardPage()
        } else if (this.currentTab === 1) {
          MarketPage()
        } else if (this.currentTab === 2) {
          AIAssistantPage()
        } else if (this.currentTab === 3) {
          PositionsPage()
        } else {
          AccountPage()
        }
      }
      .layoutWeight(1)

      // 底部导航栏
      Row() {
        this.TabBarItem('🏠', '首页', 0)
        this.TabBarItem('📈', '行情', 1)
        this.TabBarItem('🤖', 'AI', 2)
        this.TabBarItem('📊', '持仓', 3)
        this.TabBarItem('👤', '账户', 4)
      }
      .width('100%')
      .height(64)
      .backgroundColor(COLOR_CARD)
      .border({ width: { top: 1 }, color: COLOR_BORDER })
      .padding({ bottom: 8 })  // 安全区适配
    }
    .width('100%')
    .height('100%')
    .backgroundColor(COLOR_BG)
  }
}

// ─────────────── 仪表盘页 ───────────────
@Component
struct DashboardPage {
  @State totalAsset: string = '$12,680';
  @State dailyPnl: string = '+$328';
  @State pnlColor: ResourceColor = COLOR_GREEN;

  private timer: number = -1;

  aboutToAppear() {
    // 模拟实时更新
    this.timer = setInterval(() => {
      const base = 12450 + Math.random() * 500;
      this.totalAsset = '$' + Math.round(base).toLocaleString();
      const pnl = 280 + Math.random() * 100 - 50;
      this.dailyPnl = (pnl >= 0 ? '+' : '') + '$' + Math.round(pnl);
      this.pnlColor = pnl >= 0 ? COLOR_GREEN : COLOR_RED;
    }, 3000);
  }

  aboutToDisappear() {
    if (this.timer !== -1) clearInterval(this.timer);
  }

  build() {
    Scroll() {
      Column({ space: 12 }) {
        // 顶部标题栏
        Row() {
          Column() {
            Text('QuantAI')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor(COLOR_GREEN)
            Text('智能量化交易')
              .fontSize(12)
              .fontColor(COLOR_MUTED)
          }
          .alignItems(HorizontalAlign.Start)

          Blank()

          Text('🔔')
            .fontSize(22)
        }
        .width('100%')
        .padding({ top: 16, left: 16, right: 16 })

        // 资产卡片
        Column({ space: 4 }) {
          Text('总资产（USDT）')
            .fontSize(12)
            .fontColor(COLOR_MUTED)
          Text(this.totalAsset)
            .fontSize(32)
            .fontWeight(FontWeight.Bold)
            .fontColor(COLOR_TEXT)
          Row({ space: 8 }) {
            Text('今日盈亏：')
              .fontSize(13)
              .fontColor(COLOR_MUTED)
            Text(this.dailyPnl)
              .fontSize(13)
              .fontColor(this.pnlColor)
              .fontWeight(FontWeight.Bold)
          }
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })
        .alignItems(HorizontalAlign.Start)

        // 快捷操作
        Row({ space: 8 }) {
          QuickActionBtn({ icon: '⚡', label: '快速下单', color: COLOR_GREEN })
          QuickActionBtn({ icon: '🤖', label: 'AI分析', color: '#3B82F6' })
          QuickActionBtn({ icon: '📊', label: '查持仓', color: '#A855F7' })
        }
        .padding({ left: 16, right: 16 })
        .width('100%')

        // AI 每日简报
        Column({ space: 6 }) {
          Row() {
            Text('🤖 AI 每日简报')
              .fontSize(14)
              .fontWeight(FontWeight.Bold)
              .fontColor(COLOR_TEXT)
            Blank()
            Text('更多 →')
              .fontSize(12)
              .fontColor(COLOR_MUTED)
          }
          .width('100%')

          Text('BTC 维持在 $83,000 附近震荡，短期均线多头排列，建议关注 $85,000 突破方向。黄金多头持续，美元指数走弱有利贵金属。')
            .fontSize(13)
            .fontColor(COLOR_TEXT)
            .lineHeight(20)
            .opacity(0.85)
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })
        .alignItems(HorizontalAlign.Start)

        // 活跃持仓简列
        Column({ space: 6 }) {
          Text('活跃持仓')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor(COLOR_TEXT)
          MiniPositionItem({ symbol: 'BTC/USDT', side: '做多', pnl: '+$186', pct: '+2.4%', isProfit: true })
          MiniPositionItem({ symbol: 'ETH/USDT', side: '做多', pnl: '-$42',  pct: '-1.1%', isProfit: false })
          MiniPositionItem({ symbol: 'XAU/USD',  side: '做多', pnl: '+$93',  pct: '+0.8%', isProfit: true })
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })
        .alignItems(HorizontalAlign.Start)

        // 底部留白
        Blank().height(20)
      }
    }
    .width('100%')
    .height('100%')
    .scrollBar(BarState.Off)
  }
}

// ─────────────── 通用组件 ───────────────

@Component
struct QuickActionBtn {
  icon: string = '⚡';
  label: string = '';
  color: string = COLOR_GREEN;

  build() {
    Column({ space: 4 }) {
      Text(this.icon).fontSize(24)
      Text(this.label)
        .fontSize(11)
        .fontColor(COLOR_MUTED)
    }
    .layoutWeight(1)
    .height(70)
    .justifyContent(FlexAlign.Center)
    .backgroundColor(COLOR_CARD)
    .borderRadius(10)
    .border({ width: 1, color: this.color + '40' })
  }
}

@Component
struct MiniPositionItem {
  symbol: string = '';
  side: string = '';
  pnl: string = '';
  pct: string = '';
  isProfit: boolean = true;

  build() {
    Row() {
      Column() {
        Text(this.symbol)
          .fontSize(13)
          .fontWeight(FontWeight.Medium)
          .fontColor(COLOR_TEXT)
        Text(this.side)
          .fontSize(11)
          .fontColor(this.isProfit ? COLOR_GREEN : COLOR_RED)
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      Column() {
        Text(this.pnl)
          .fontSize(13)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.isProfit ? COLOR_GREEN : COLOR_RED)
        Text(this.pct)
          .fontSize(11)
          .fontColor(this.isProfit ? COLOR_GREEN : COLOR_RED)
          .opacity(0.7)
      }
      .alignItems(HorizontalAlign.End)
    }
    .width('100%')
    .padding({ top: 8, bottom: 8 })
    .border({ width: { bottom: 1 }, color: COLOR_BORDER })
  }
}
