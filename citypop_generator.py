#!/usr/bin/env python3
"""Generate daily city pop style lyrics themed around Japanese cities.

This script uses the current date (or a provided date) to create a
deterministic seed, ensuring that running it once per day yields a new but
reproducible lyric and SUNO style prompt.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import random
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class CityProfile:
    name: str
    prefecture: str
    landmarks: tuple[str, ...]
    night_views: tuple[str, ...]
    sensory: tuple[str, ...]
    transport: tuple[str, ...]
    phrases: tuple[str, ...]
    colors: tuple[str, ...]


CITY_PROFILES: tuple[CityProfile, ...] = (
    CityProfile(
        name="東京",
        prefecture="東京都",
        landmarks=("渋谷スクランブル", "代々木公園", "六本木ヒルズ", "東京タワー"),
        night_views=("雨に滲んだネオン", "首都高の流星", "ビルの窓が描く星座", "湾岸のミラーボール"),
        sensory=("スチームの立つ屋台", "アスファルトの熱気", "レコードから溢れるクラップ", "深夜のラジオ"),
        transport=("山手線", "都営大江戸線", "深夜バス"),
        phrases=("midnight cruising", "sparkling skyline", "lost in translation", "Tokyo twilight"),
        colors=("コバルトブルー", "フューシャ", "エメラルド", "琥珀"),
    ),
    CityProfile(
        name="横浜",
        prefecture="神奈川県",
        landmarks=("みなとみらい", "赤レンガ倉庫", "大桟橋", "山下公園"),
        night_views=("潮風を抱く摩天楼", "観覧車が刻む鼓動", "波間に揺れる街灯", "港のドレスコード"),
        sensory=("潮の香り", "サックスのリフ", "カクテルのグラス", "ピアノバーのざわめき"),
        transport=("みなとみらい線", "シーバス", "東海道線"),
        phrases=("ocean drive", "bay area fantasy", "harbor light", "neon breeze"),
        colors=("ターコイズ", "クリムゾン", "サンセットオレンジ", "パールホワイト"),
    ),
    CityProfile(
        name="札幌",
        prefecture="北海道",
        landmarks=("大通公園", "すすきの", "藻岩山", "時計台"),
        night_views=("粉雪が光るアーケード", "暖色のガス灯", "霧に揺れるテールライト", "星降る空中歩道"),
        sensory=("白樺の香り", "スノウクリスタル", "シンセのパッド", "ホットラムの蒸気"),
        transport=("札幌市電", "南北線", "深夜タクシー"),
        phrases=("northern glow", "powder night", "frosty groove", "aurora line"),
        colors=("アイスブルー", "シャンパンゴールド", "ラベンダー", "ダークインディゴ"),
    ),
    CityProfile(
        name="京都",
        prefecture="京都府",
        landmarks=("鴨川", "祇園", "東山", "先斗町"),
        night_views=("石畳を照らす行灯", "格子窓に揺れる灯影", "山際の濃紺", "川面の反射"),
        sensory=("抹茶の苦み", "三味線の余韻", "夏夜の風鈴", "浴衣の香り"),
        transport=("京阪電車", "嵐電", "タクシー"),
        phrases=("twilight kimono", "retro future", "silent river", "moonlit alley"),
        colors=("藍", "朱", "亜麻色", "群青"),
    ),
    CityProfile(
        name="名古屋",
        prefecture="愛知県",
        landmarks=("栄", "オアシス21", "名古屋城", "大須"),
        night_views=("テレビ塔のダイヤモンド", "高速道路のループ", "ミラーガラスの銀河", "深夜の屋台"),
        sensory=("手羽先のスパイス", "アナログシンセ", "クラブのビート", "味噌の香り"),
        transport=("東山線", "名城線", "リニモ"),
        phrases=("golden avenue", "urban maze", "night mirage", "fever line"),
        colors=("アンバー", "エレクトリックブルー", "プラチナ", "シトラス"),
    ),
    CityProfile(
        name="大阪",
        prefecture="大阪府",
        landmarks=("中之島", "道頓堀", "梅田スカイビル", "天保山"),
        night_views=("グリッターな川面", "グリコサインの残像", "高架下のトワイライト", "大観覧車の軌跡"),
        sensory=("粉もんの香り", "ファンキーなベース", "笑い声のサンプリング", "ナイトクルーズの風"),
        transport=("御堂筋線", "阪神電車", "水上バス"),
        phrases=("soulful skyline", "urban carnival", "neon heartbeat", "midnight takoyaki"),
        colors=("マゼンタ", "アジュール", "シャンパン", "バイオレット"),
    ),
    CityProfile(
        name="福岡",
        prefecture="福岡県",
        landmarks=("天神", "中洲", "大濠公園", "百道浜"),
        night_views=("屋台のランタン", "川に滲む光", "シーサイドの残光", "ビートに揺れる橋"),
        sensory=("明太子の辛味", "潮風とシンセ", "クラブのダウンビート", "泡盛の香り"),
        transport=("西鉄", "空港線", "ベイエリアフェリー"),
        phrases=("sunset drive", "night blossom", "fukuoka groove", "afterglow"),
        colors=("サーモンピンク", "インディゴ", "ターコイズ", "ルビー"),
    ),
    CityProfile(
        name="金沢",
        prefecture="石川県",
        landmarks=("ひがし茶屋街", "兼六園", "近江町市場", "金沢駅"),
        night_views=("雨音とガス灯", "格子戸のシルエット", "しっとりした路面", "鼓門のライトアップ"),
        sensory=("和傘のしずく", "ジャズのピアノ", "加賀友禅の手触り", "柚子の香り"),
        transport=("北陸新幹線", "路線バス", "タクシー"),
        phrases=("amber rain", "silent swing", "kanazawa moon", "raindrop groove"),
        colors=("翡翠", "朽葉色", "ローズゴールド", "墨"),
    ),
    CityProfile(
        name="神戸",
        prefecture="兵庫県",
        landmarks=("北野坂", "ハーバーランド", "メリケンパーク", "南京町"),
        night_views=("ポートタワーの鼓動", "山手の夜景", "海霧に浮かぶビル", "石畳を濡らす月光"),
        sensory=("ジャズバーのブラス", "港町のソルト", "エスプレッソの香り", "潮風と香水"),
        transport=("ポートライナー", "阪急電車", "神戸市営地下鉄"),
        phrases=("harbor swing", "moonlit slope", "velvet port", "silent cruise"),
        colors=("ボルドー", "ミッドナイトブルー", "シルバー", "ターコイズ"),
    ),
    CityProfile(
        name="那覇",
        prefecture="沖縄県",
        landmarks=("国際通り", "首里城", "波上宮", "北谷サンセットビーチ"),
        night_views=("潮風に揺れるネオンサイン", "月光浴するココナッツ", "砂に描く光のライン", "星砂のきらめき"),
        sensory=("シンセスチールパン", "トロピカルな風", "泡盛レモン", "打ち寄せる波音"),
        transport=("ゆいレール", "国際通りのタクシー", "フェリー"),
        phrases=("island boogie", "tropical midnight", "coral groove", "sugar wave"),
        colors=("ターコイズ", "サンゴピンク", "サンライトイエロー", "ミッドナイトネイビー"),
    ),
)


VERSE_MOODS = (
    "淡く滲む", "胸が躍る", "忘れられない", "切なく響く", "スロウに弾む",
    "秘密めいた", "レトロフューチャーな", "眩暈を誘う", "甘く香る", "夜更けの",
)

CHORUS_CALLS = (
    "抱きしめてよ", "離さないで", "夢のままで", "踊り続けて", "耳元で",
    "このまま", "夜明けまで", "駆け抜けて", "連れ出して", "忘れさせて",
)

BRIDGE_VIBES = (
    "アナログテープを巻き戻すように", "夜明け前の潮騒がリズムを刻む",
    "胸の鼓動がクリックを追い越す", "流星群がバッキングコーラスになる",
    "古いシンセが溜息を漏らす", "タクシーのライトが拍を刻む",
)

OUTRO_LINES = (
    "フェードアウトする君の影と手を振る",
    "ビートが止んでも夜は終わらない",
    "朝焼けのグラデーションに溶けていく",
    "最後のコードに願いを重ねる",
)

BPM_CHOICES = ("96", "100", "102", "104", "108")
GROOVES = (
    "シティポップ", "80sフュージョン", "ブギーファンク", "ドリームポップ", "モダンAOR"
)
RHYTHM_SECTIONS = (
    "タイトなドラム", "リムショットが煌めくドラム", "跳ねるシンコペーション", "ローズピアノのコンピング",
)
BASS_LINES = (
    "スラップベース", "シンセベース", "ウォームなエレキベース", "モノフォニックシンセベース",
)
CHORD_TEXTURES = (
    "9thを散りばめたコードワーク", "シックなテンションコード", "ローズピアノとギターのユニゾン",
    "ジャジーなカッティング", "煌めくローズピアノ",
)
LEAD_ELEMENTS = (
    "ブリージーな女性ボーカル", "スモーキーな男性ボーカル", "デュエットボーカル", "ヴォコーダーハーモニー",
)
FX_ELEMENTS = (
    "リバーブを深くかけたサックスソロ", "コーラスの効いたギター", "テープエコーの余韻", "シンセストリングスの広がり",
    "ナイトドライブのSE",
)


def _make_seed_from_date(target_date: _dt.date) -> int:
    """Return a deterministic seed derived from the provided date."""
    digest = hashlib.sha256(target_date.isoformat().encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def choose_city(rng: random.Random) -> CityProfile:
    return rng.choice(CITY_PROFILES)


def _pick(rng: random.Random, options: tuple[str, ...]) -> str:
    return rng.choice(options)


def build_verse(rng: random.Random, city: CityProfile) -> str:
    lines = [
        f"{_pick(rng, VERSE_MOODS)}{_pick(rng, city.landmarks)}で目が合う",
        f"{_pick(rng, city.night_views)}が鼓動を追い越して",
        f"{_pick(rng, city.sensory)}が合図を送る",
        f"{_pick(rng, city.transport)}は{_pick(rng, VERSE_MOODS)}ループを描く",
    ]
    return "\n".join(lines)


def build_second_verse(rng: random.Random, city: CityProfile) -> str:
    lines = [
        f"{city.colors[0]}の街角で秘密を重ねて",
        f"{_pick(rng, city.sensory)}が指先を染める",
        f"{_pick(rng, city.landmarks[1:])}へ続くムーンライト",
        f"{_pick(rng, VERSE_MOODS)}二人だけのハーモニー",
    ]
    return "\n".join(lines)


def build_pre_chorus(rng: random.Random, city: CityProfile) -> str:
    lines = [
        f"{_pick(rng, city.night_views)}がカウントダウン",
        f"{_pick(rng, city.phrases)}の合図で",
        f"息を止めたまま{_pick(rng, CHORUS_CALLS)}",
    ]
    return "\n".join(lines)


def build_chorus(rng: random.Random, city: CityProfile) -> str:
    lines = [
        f"{city.name} midnight {_pick(rng, city.phrases)}",
        f"光る{_pick(rng, city.landmarks)}に身を委ね",
        f"{_pick(rng, CHORUS_CALLS)}この瞬間をループさせて",
        f"{city.prefecture}の星が踊り続ける",
    ]
    return "\n".join(lines)


def build_bridge(rng: random.Random, city: CityProfile) -> str:
    lines = [
        _pick(rng, BRIDGE_VIBES),
        f"{_pick(rng, city.transport)}の軋みがバックビート",
        f"{_pick(rng, city.colors)}のきらめきに包まれて",
    ]
    return "\n".join(lines)


def build_outro(rng: random.Random) -> str:
    return _pick(rng, OUTRO_LINES)


def build_style_prompt(rng: random.Random, city: CityProfile, bpm: str | None = None) -> str:
    bpm_value = bpm or _pick(rng, BPM_CHOICES)
    style_parts = [
        f"City Pop {bpm_value} BPM",
        f"{_pick(rng, GROOVES)}グルーヴ",
        _pick(rng, RHYTHM_SECTIONS),
        _pick(rng, BASS_LINES),
        _pick(rng, CHORD_TEXTURES),
        _pick(rng, LEAD_ELEMENTS),
        _pick(rng, FX_ELEMENTS),
        f"{city.name} {_pick(rng, city.phrases)} atmosphere",
    ]
    return ", ".join(style_parts)


def generate_daily_lyric(target_date: _dt.date) -> tuple[CityProfile, str, str]:
    seed = _make_seed_from_date(target_date)
    rng = random.Random(seed)
    city = choose_city(rng)
    sections = {
        "Verse 1": build_verse(rng, city),
        "Verse 2": build_second_verse(rng, city),
        "Pre-Chorus": build_pre_chorus(rng, city),
        "Chorus": build_chorus(rng, city),
        "Bridge": build_bridge(rng, city),
        "Outro": build_outro(rng),
    }

    lyric_blocks = [f"[{name}]\n{content}" for name, content in sections.items()]
    lyric_text = "\n\n".join(lyric_blocks)
    style_prompt = build_style_prompt(rng, city)
    return city, lyric_text, style_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily city pop lyrics and SUNO style prompt")
    parser.add_argument(
        "--date",
        type=lambda value: _dt.datetime.strptime(value, "%Y-%m-%d").date(),
        help="Target date (YYYY-MM-DD). Defaults to today.",
    )
    args = parser.parse_args()

    target_date = args.date or _dt.date.today()
    city, lyric_text, style_prompt = generate_daily_lyric(target_date)

    header = dedent(
        f"""
        ==== City Pop Daily ====
        Date: {target_date.isoformat()}
        Theme City: {city.name} ({city.prefecture})
        """
    ).strip()

    print(header)
    print()
    print(lyric_text)
    print()
    print("SUNO Style Prompt:")
    print(style_prompt)


if __name__ == "__main__":
    main()
