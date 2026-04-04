// QuantAI HarmonyOS NEXT - 持仓页 + 账户页
// ArkTS + ArkUI

const COLOR_BG = '#0A1628';
const COLOR_CARD = '#111F35';
const COLOR_GREEN = '#00C896';
const COLOR_RED = '#FF4B6E';
const COLOR_TEXT = '#E8F4FF';
const COLOR_MUTED = '#6B8DB0';
const COLOR_BORDER = '#1E3050';

interface Position {
  symbol: string;
  side: string;
  size: string;
  entryPrice: string;
  currentPrice: string;
  pnl: string;
  pnlPct: string;
  isProfit: boolean;
}

// ─────────────── 持仓页 ───────────────
@Component
export struct PositionsPage {
  @State positions: Position[] = [
    { symbol: 'BTC/USDT', side: '做多', size: '0.1 BTC', entryPrice: '$82,800', currentPrice: '$83,250', pnl: '+$45', pnlPct: '+0.54%', isProfit: true },
    { symbol: 'ETH/USDT', side: '做多', size: '1.0 ETH', entryPrice: '$1,858',  currentPrice: '$1,842',  pnl: '-$16', pnlPct: '-0.86%', isProfit: false },
    { symbol: 'XAU/USD',  side: '做多', size: '0.5 oz',  entryPrice: '$2,926',  currentPrice: '$2,942',  pnl: '+$8',  pnlPct: '+0.55%', isProfit: true },
  ];
  @State totalPnl: string = '+$37';
  @State totalPnlIsProfit: boolean = true;

  build() {
    Column() {
      // 标题
      Row() {
        Text('持仓管理')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor(COLOR_TEXT)
        Blank()
        Button('一键平仓')
          .fontSize(12)
          .height(32)
          .backgroundColor(COLOR_RED + '20')
          .fontColor(COLOR_RED)
          .borderRadius(16)
          .border({ width: 1, color: COLOR_RED + '60' })
      }
      .width('100%')
      .padding({ top: 16, left: 16, right: 16, bottom: 8 })

      // 汇总卡片
      Row({ space: 16 }) {
        Column() {
          Text('持仓数').fontSize(11).fontColor(COLOR_MUTED)
          Text(this.positions.length.toString()).fontSize(24).fontWeight(FontWeight.Bold).fontColor(COLOR_TEXT)
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)

        Column() {
          Text('总浮盈').fontSize(11).fontColor(COLOR_MUTED)
          Text(this.totalPnl)
            .fontSize(24)
            .fontWeight(FontWeight.Bold)
            .fontColor(this.totalPnlIsProfit ? COLOR_GREEN : COLOR_RED)
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)

        Column() {
          Text('占用保证金').fontSize(11).fontColor(COLOR_MUTED)
          Text('$856').fontSize(24).fontWeight(FontWeight.Bold).fontColor(COLOR_TEXT)
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)
      }
      .width('100%')
      .padding(16)
      .backgroundColor(COLOR_CARD)
      .margin({ left: 16, right: 16, bottom: 12 })
      .borderRadius(12)

      // 持仓列表
      List({ space: 8 }) {
        ForEach(this.positions, (pos: Position, index: number) => {
          ListItem() {
            Column({ space: 8 }) {
              // 品种 + 方向
              Row() {
                Text(pos.symbol)
                  .fontSize(15)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(COLOR_TEXT)
                Text(pos.side)
                  .fontSize(11)
                  .fontColor(pos.isProfit ? COLOR_GREEN : COLOR_RED)
                  .backgroundColor(pos.isProfit ? COLOR_GREEN + '20' : COLOR_RED + '20')
                  .padding({ top: 3, bottom: 3, left: 8, right: 8 })
                  .borderRadius(10)
                  .margin({ left: 8 })
                Blank()
                Text(pos.pnl)
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(pos.isProfit ? COLOR_GREEN : COLOR_RED)
              }

              // 价格信息
              Row() {
                Text(`入场：${pos.entryPrice}`)
                  .fontSize(12)
                  .fontColor(COLOR_MUTED)
                Text('→').fontSize(12).fontColor(COLOR_MUTED).margin({ left: 8, right: 8 })
                Text(`现价：${pos.currentPrice}`)
                  .fontSize(12)
                  .fontColor(COLOR_TEXT)
                Blank()
                Text(pos.pnlPct)
                  .fontSize(12)
                  .fontColor(pos.isProfit ? COLOR_GREEN : COLOR_RED)
              }

              // 操作按钮
              Row({ space: 8 }) {
                Button('平仓')
                  .fontSize(12)
                  .height(30)
                  .layoutWeight(1)
                  .backgroundColor(COLOR_RED + '20')
                  .fontColor(COLOR_RED)
                  .borderRadius(8)
                Button('AI分析')
                  .fontSize(12)
                  .height(30)
                  .layoutWeight(1)
                  .backgroundColor(COLOR_CARD)
                  .fontColor(COLOR_MUTED)
                  .borderRadius(8)
                  .border({ width: 1, color: COLOR_BORDER })
              }
            }
            .width('100%')
            .padding(16)
            .backgroundColor(COLOR_CARD)
            .borderRadius(12)
            .margin({ left: 16, right: 16 })
          }
        })
      }
      .layoutWeight(1)
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor(COLOR_BG)
  }
}

// ─────────────── 账户页 ───────────────
@Component
export struct AccountPage {
  @State stopLossEnabled: boolean = true;
  @State autoCloseEnabled: boolean = true;
  @State emailNotify: boolean = true;

  build() {
    Scroll() {
      Column({ space: 12 }) {
        Text('账户设置')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor(COLOR_TEXT)
          .padding({ top: 16, left: 16 })
          .alignSelf(ItemAlign.Start)

        // 用户信息卡片
        Row({ space: 12 }) {
          Text('👤')
            .fontSize(40)
            .backgroundColor(COLOR_CARD)
            .padding(8)
            .borderRadius(40)
          Column({ space: 4 }) {
            Text('交易员 001')
              .fontSize(16)
              .fontWeight(FontWeight.Bold)
              .fontColor(COLOR_TEXT)
            Text('Pro 会员')
              .fontSize(12)
              .fontColor(COLOR_GREEN)
            Text('到期：2026-12-31')
              .fontSize(11)
              .fontColor(COLOR_MUTED)
          }
          .alignItems(HorizontalAlign.Start)
          .layoutWeight(1)

          Button('升级')
            .fontSize(12)
            .height(32)
            .backgroundColor(COLOR_GREEN)
            .fontColor('#0A1628')
            .borderRadius(16)
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })

        // 券商连接
        Column({ space: 8 }) {
          Text('已连接券商')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor(COLOR_TEXT)
          Row() {
            Text('🟡 Binance')
              .fontSize(13)
              .fontColor(COLOR_TEXT)
            Blank()
            Text('已连接 ✓')
              .fontSize(12)
              .fontColor(COLOR_GREEN)
          }
          .padding({ top: 12, bottom: 12 })
          .border({ width: { bottom: 1 }, color: COLOR_BORDER })
          Row() {
            Text('⚫ OKX')
              .fontSize(13)
              .fontColor(COLOR_TEXT)
            Blank()
            Button('+ 连接')
              .fontSize(12)
              .height(28)
              .backgroundColor(COLOR_CARD)
              .fontColor(COLOR_GREEN)
              .borderRadius(14)
              .border({ width: 1, color: COLOR_GREEN + '60' })
          }
          .padding({ top: 12 })
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })
        .alignItems(HorizontalAlign.Start)

        // 风控设置
        Column({ space: 12 }) {
          Text('风控设置')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor(COLOR_TEXT)

          SettingToggleItem({
            label: '自动止损',
            sublabel: '亏损超过5%自动平仓',
            isOn: this.stopLossEnabled,
            onChange: (val: boolean) => { this.stopLossEnabled = val; }
          })

          SettingToggleItem({
            label: '自动平仓',
            sublabel: '达到止盈目标自动出场',
            isOn: this.autoCloseEnabled,
            onChange: (val: boolean) => { this.autoCloseEnabled = val; }
          })

          SettingToggleItem({
            label: '邮件通知',
            sublabel: '下单/止损时发送邮件',
            isOn: this.emailNotify,
            onChange: (val: boolean) => { this.emailNotify = val; }
          })
        }
        .width('100%')
        .padding(16)
        .backgroundColor(COLOR_CARD)
        .borderRadius(12)
        .margin({ left: 16, right: 16 })
        .alignItems(HorizontalAlign.Start)

        // 退出登录
        Button('退出登录')
          .width('100%')
          .height(48)
          .backgroundColor(COLOR_RED + '20')
          .fontColor(COLOR_RED)
          .borderRadius(12)
          .margin({ left: 16, right: 16 })
          .fontSize(15)

        Blank().height(20)
      }
    }
    .width('100%')
    .height('100%')
    .scrollBar(BarState.Off)
    .backgroundColor(COLOR_BG)
  }
}

@Component
struct SettingToggleItem {
  label: string = '';
  sublabel: string = '';
  @Prop isOn: boolean = false;
  onChange: (val: boolean) => void = () => {};

  build() {
    Row() {
      Column({ space: 2 }) {
        Text(this.label)
          .fontSize(14)
          .fontColor(COLOR_TEXT)
        Text(this.sublabel)
          .fontSize(11)
          .fontColor(COLOR_MUTED)
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)

      Toggle({ type: ToggleType.Switch, isOn: this.isOn })
        .selectedColor(COLOR_GREEN)
        .onChange((isOn: boolean) => { this.onChange(isOn); })
    }
    .width('100%')
    .padding({ top: 8, bottom: 8 })
    .border({ width: { bottom: 1 }, color: COLOR_BORDER })
  }
}
