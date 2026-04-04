// QuantAI HarmonyOS NEXT - 行情页
// ArkTS + ArkUI

const COLOR_BG = '#0A1628';
const COLOR_CARD = '#111F35';
const COLOR_GREEN = '#00C896';
const COLOR_RED = '#FF4B6E';
const COLOR_TEXT = '#E8F4FF';
const COLOR_MUTED = '#6B8DB0';
const COLOR_BORDER = '#1E3050';

interface QuoteItem {
  symbol: string;
  price: string;
  change: string;
  isUp: boolean;
  type: string;
}

@Component
export struct MarketPage {
  @State activeCategory: string = 'all';
  @State quotes: QuoteItem[] = [
    { symbol: 'BTC/USDT',  price: '$83,250',  change: '+2.4%',  isUp: true,  type: 'crypto' },
    { symbol: 'ETH/USDT',  price: '$1,842',   change: '-0.8%',  isUp: false, type: 'crypto' },
    { symbol: 'SOL/USDT',  price: '$128.5',   change: '+5.2%',  isUp: true,  type: 'crypto' },
    { symbol: 'BNB/USDT',  price: '$595',     change: '+1.1%',  isUp: true,  type: 'crypto' },
    { symbol: 'EUR/USD',   price: '1.0831',   change: '-0.12%', isUp: false, type: 'forex'  },
    { symbol: 'GBP/USD',   price: '1.2645',   change: '+0.08%', isUp: true,  type: 'forex'  },
    { symbol: 'USD/JPY',   price: '149.82',   change: '+0.35%', isUp: true,  type: 'forex'  },
    { symbol: 'XAU/USD',   price: '$2,942',   change: '+0.64%', isUp: true,  type: 'metal'  },
    { symbol: 'CL/USD',    price: '$71.25',   change: '-1.2%',  isUp: false, type: 'energy' },
    { symbol: 'NQ/USD',    price: '19,856',   change: '+0.92%', isUp: true,  type: 'index'  },
  ];

  private categories = [
    { key: 'all', label: '全部' },
    { key: 'crypto', label: '加密' },
    { key: 'forex', label: '外汇' },
    { key: 'metal', label: '贵金属' },
    { key: 'energy', label: '能源' },
    { key: 'index', label: '指数' },
  ];

  get filteredQuotes(): QuoteItem[] {
    if (this.activeCategory === 'all') return this.quotes;
    return this.quotes.filter(q => q.type === this.activeCategory);
  }

  build() {
    Column() {
      // 标题
      Text('市场行情')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor(COLOR_TEXT)
        .padding({ top: 16, left: 16, bottom: 8 })
        .alignSelf(ItemAlign.Start)

      // 分类筛选
      Scroll() {
        Row({ space: 8 }) {
          ForEach(this.categories, (cat: { key: string, label: string }) => {
            Text(cat.label)
              .fontSize(13)
              .fontColor(this.activeCategory === cat.key ? '#0A1628' : COLOR_MUTED)
              .backgroundColor(this.activeCategory === cat.key ? COLOR_GREEN : COLOR_CARD)
              .padding({ top: 6, bottom: 6, left: 14, right: 14 })
              .borderRadius(20)
              .onClick(() => { this.activeCategory = cat.key; })
          })
        }
        .padding({ left: 16, right: 16 })
      }
      .scrollable(ScrollDirection.Horizontal)
      .scrollBar(BarState.Off)
      .height(44)

      // 行情列表
      List({ space: 1 }) {
        ForEach(this.filteredQuotes, (item: QuoteItem) => {
          ListItem() {
            Row() {
              Column() {
                Text(item.symbol)
                  .fontSize(14)
                  .fontWeight(FontWeight.Medium)
                  .fontColor(COLOR_TEXT)
                Text(item.type.toUpperCase())
                  .fontSize(10)
                  .fontColor(COLOR_MUTED)
                  .margin({ top: 2 })
              }
              .alignItems(HorizontalAlign.Start)

              Blank()

              Column() {
                Text(item.price)
                  .fontSize(14)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(COLOR_TEXT)
                Text(item.change)
                  .fontSize(12)
                  .fontColor(item.isUp ? COLOR_GREEN : COLOR_RED)
                  .margin({ top: 2 })
              }
              .alignItems(HorizontalAlign.End)
            }
            .width('100%')
            .padding({ top: 14, bottom: 14, left: 16, right: 16 })
            .backgroundColor(COLOR_CARD)
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
