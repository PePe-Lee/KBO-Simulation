import pandas as pd
import random
from typing import List, Dict, Any

# --- 데이터 로드 ---
def load_pitcher_data(file_path: str) -> List[Dict[str, Any]]:
    """투수 데이터를 로드하여 리스트로 반환."""
    pitcher_data = pd.read_excel(file_path)
    pitchers = []
    for _, row in pitcher_data.iterrows():
        team_name = row.get("팀")
        if pd.isna(team_name) or not team_name.strip():  # 빈 값 또는 공백 검사
            continue
        pitchers.append({
            "name": row["선수명"],
            "team": team_name.strip(),  # 공백 제거
            "position": row["포지션"],
            "weather": row["날씨"],
            "stats": {
                "ERA": row.get("ERA", 0),
                "볼넷/9": row.get("볼넷/9", 0),
                "삼진/9": row.get("삼진/9", 0),
            }
        })
    return pitchers

def load_batter_data(file_path: str) -> List[Dict[str, Any]]:
    """타자 데이터를 로드하여 리스트로 반환."""
    batter_data = pd.read_excel(file_path)
    batters = []
    for _, row in batter_data.iterrows():
        team_name = row.get("팀")
        if pd.isna(team_name) or not team_name.strip():  # 빈 값 또는 공백 검사
            continue
        batters.append({
            "name": row["선수명"],
            "team": team_name.strip(),  # 공백 제거
            "position": row["포지션"],
            "weather": row["날씨"],
            "stats": {
                "볼넷%": row.get("볼넷%", 0),
                "삼진%": row.get("삼진%", 0),
                "wRC": row.get("wRC", 0),
                "타율": row.get("타율", 0),
                "타수": row.get("타수", 0),
                "안타": row.get("안타", 0),
                "단타": row.get("단타", 0),
                "2루타": row.get("2루타", 0),
                "3루타": row.get("3루타", 0),
                "홈런": row.get("홈런", 0),
            }
        })
    return batters


def group_by_team(pitchers: List[Dict[str, Any]], batters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """투수와 타자 데이터를 팀별로 그룹화."""
    teams = {}
    for pitcher in pitchers:
        team = pitcher["team"]
        if not team:  # 팀 이름이 없으면 제외
            continue
        if team not in teams:
            teams[team] =  {"team_name": team, "batters": [], "pitchers": {"starters": [], "relievers": []}}
        if pitcher["position"] == "선발":
            teams[team]["pitchers"]["starters"].append(pitcher)
        else:
            teams[team]["pitchers"]["relievers"].append(pitcher)

    for batter in batters:
        team = batter["team"]
        if not team:  # 팀 이름이 없으면 제외
            continue
        if team not in teams:
            teams[team] = {"team_name": team, "batters": [], "pitchers": []}
        teams[team]["batters"].append(batter)

    # 빈 팀 필터링
    return {team: data for team, data in teams.items() if data["batters"] and data["pitchers"]}


def print_batter_list_by_position(batters: List[Dict[str, Any]]):
    """타자 명단을 포지션별로 정렬하여 출력 (볼넷%, 삼진%, wRC, 타율 포함)."""
    positions = {"포수": [], "내야수": [], "외야수": []}

    # 포지션별로 분류
    for batter in batters:
        position = batter["position"]
        if position in positions:
            positions[position].append(batter)
        else:
            positions.setdefault("기타", []).append(batter)

    # 포지션별 출력
    print("\n--- 타자 명단 (포지션별) ---")
    for position, players in positions.items():
        print(f"\n[{position}]")
        print(f"{'이름':<10} {'날씨':<10} {'볼넷%':<10} {'삼진%':<8} {'wRC':<8} {'타율':<7} {'타수':<6} {'안타':<6} {'단타':<6} {'2루타':<6} {'3루타':<6} {'홈런':<6}")
        print("-" * 110)
        for batter in players:
            stats = batter["stats"]
            print(
                f"{batter['name']:<10} {batter['weather']:<10} {stats['볼넷%']:<10.1f} {stats['삼진%']:<10.1f} {stats['wRC']:<8.1f} {stats['타율']:<8.3f} {stats['타수']:<6} {stats['안타']:<8} {stats['단타']:<7} {stats['2루타']:<8} {stats['3루타']:<7} {stats['홈런']:<8}")


def print_pitcher_list_by_position(pitchers: List[Dict[str, Any]]):
    """투수 명단을 포지션별로 정렬하여 출력 (ERA, 볼넷/9, 삼진/9 포함)."""
    positions = {"선발": [], "불펜": []}

    # 포지션별로 분류
    for pitcher in pitchers:
        position = pitcher["position"]
        if position in positions:
            positions[position].append(pitcher)
        else:
            positions.setdefault("기타", []).append(pitcher)

    # 포지션별 출력
    print("\n--- 투수 명단 (포지션별) ---")
    for position, players in positions.items():
        print(f"\n[{position}]")
        print(f"{'이름':<10} {'ERA':<10} {'볼넷/9':<10} {'삼진/9':<7} {'날씨':<10}")
        print("-" * 50)
        for pitcher in players:
            stats = pitcher["stats"]
            print(f"{pitcher['name']:<10} {stats['ERA']:<10.2f} {stats['볼넷/9']:<10.2f} {stats['삼진/9']:<9.2f} {pitcher['weather']:<10}")


def print_selected_pitchers(starters: List[Dict[str, Any]], relievers: List[Dict[str, Any]]):
    """선택된 선발 및 불펜 투수를 순서대로 출력."""
    print("\n--- 선택된 투수 명단 ---")

    # 선발 투수 출력
    print("\n[선발]")
    print(f"{'순번':<5} {'이름':<10} {'ERA':<10} {'볼넷/9':<8} {'삼진/9':<7} {'날씨':<10}")
    print("-" * 60)
    for i, pitcher in enumerate(starters, 1):
        stats = pitcher["stats"]
        print(f"{i:<5} {pitcher['name']:<10} {stats['ERA']:<10.2f} {stats['볼넷/9']:<10.2f} {stats['삼진/9']:<9.2f} {pitcher['weather']:<10}")

    # 불펜 투수 출력
    print("\n[불펜]")
    print(f"{'순번':<5} {'이름':<10} {'ERA':<10} {'볼넷/9':<8} {'삼진/9':<7} {'날씨':<10}")
    print("-" * 60)
    for i, pitcher in enumerate(relievers, 1):
        stats = pitcher["stats"]
        print(f"{i:<5} {pitcher['name']:<10} {stats['ERA']:<10.2f} {stats['볼넷/9']:<10.2f} {stats['삼진/9']:<9.2f} {pitcher['weather']:<10}")


# --- 유저 팀 구성 ---
def select_user_team(team_data: Dict[str, Any]) -> Dict[str, Any]:
    """유저가 팀을 선택하고 선수를 구성."""
    teams = list(team_data.keys())
    print("\n사용 가능한 팀 목록:")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team}")

    while True:
        try:
            choice = int(input("\n플레이할 팀 번호를 선택하세요: "))
            if 1 <= choice <= len(teams):
                selected_team_name = teams[choice - 1]
                break
            else:
                print("올바른 번호를 입력하세요.")
        except ValueError:
            print("숫자를 입력해주세요.")

    user_team = team_data[selected_team_name]
    print(f"\n선택한 팀: {selected_team_name}")

    # 타자 선택
    print("\n타자 명단:")
    # 포지션별 타자 명단 출력
    print_batter_list_by_position(user_team["batters"])

    required_positions = {"포수": 1, "내야수": 4, "외야수": 3}
    selected_batters = []

    for position, count in required_positions.items():
        print(f"\n{position}에서 {count}명 선택하세요.")
        while len([b for b in selected_batters if b["position"] == position]) < count:
            choice = input(f"{position} 선수 이름: ")
            batter = next((b for b in user_team["batters"] if b["name"] == choice), None)
            if batter and batter not in selected_batters and batter["position"] == position:
                selected_batters.append(batter)
            else:
                print("올바른 선수 이름을 입력하세요.")

    # 나머지 후보 타자 선택
    print("\n후보 타자 6명을 선택하세요.")
    while len(selected_batters) < 14:
        choice = input("후보 타자 이름: ")
        batter = next((b for b in user_team["batters"] if b["name"] == choice), None)
        if batter and batter not in selected_batters:
            selected_batters.append(batter)
        else:
            print("올바른 선수 이름을 입력하세요.")

    print("\n선택한 타자 명단:")
    for batter in selected_batters:
        print(batter["name"])

    # 투수 선택
    print("\n투수 명단:")
    # 포지션별 투수 명단 출력
    all_pitchers = user_team["pitchers"]["starters"] + user_team["pitchers"]["relievers"]
    print_pitcher_list_by_position(all_pitchers)

    # 선발 투수 선택
    print("\n선발 5명을 선택하세요.(선택하는 순서가 선발 순서)")
    starters = []
    while len(starters) < 5:
        choice = input("선발 투수 이름: ")
        pitcher = next((p for p in user_team["pitchers"]["starters"] if p["name"] == choice), None)
        if pitcher and pitcher not in starters:
            starters.append(pitcher)
        else:
            print("올바른 투수 이름을 입력하세요.")

          # 불펜 투수 선택
    print("\n불펜 6명을 선택하세요.(선택하는 순서가 불펜 순서)")
    relievers = []
    while len(relievers) < 6:
        choice = input("불펜 투수 이름: ")
        pitcher = next((p for p in user_team["pitchers"]["relievers"] if p["name"] == choice), None)
        if pitcher and pitcher not in relievers:
            relievers.append(pitcher)
        else:
            print("올바른 투수 이름을 입력하세요.")


    return {
        "team_name": user_team["team_name"],
        "batters": selected_batters,
        "pitchers": {"starters": starters, "relievers":  relievers}
    }


def auto_configure_teams(team_data: Dict[str, Any], user_team_name: str) -> Dict[str, Any]:
    """나머지 9개 팀을 AI_team [팀명] 형식으로 구성."""
    ai_teams = {}  # AI 팀 데이터를 저장할 딕셔너리

    for team_name, team in team_data.items():
        if team_name == user_team_name:
            continue  # 사용자 팀은 건너뛰기

        # 타자 구성
        catchers = [batter for batter in team["batters"] if batter["position"] == "포수"]
        top_catcher = sorted(catchers, key=lambda x: x["stats"].get("wRC", 0), reverse=True)[:1]

        infielders = [batter for batter in team["batters"] if batter["position"] == "내야수"]
        top_infielders = sorted(infielders, key=lambda x: x["stats"].get("wRC", 0), reverse=True)[:4]

        outfielders = [batter for batter in team["batters"] if batter["position"] == "외야수"]
        top_outfielders = sorted(outfielders, key=lambda x: x["stats"].get("wRC", 0), reverse=True)[:3]

        remaining_batters = [
            batter for batter in team["batters"]
            if batter not in (top_catcher + top_infielders + top_outfielders)
        ]
        top_remaining_batters = sorted(remaining_batters, key=lambda x: x["stats"].get("wRC", 0), reverse=True)[:6]

        batters = top_catcher + top_infielders + top_outfielders + top_remaining_batters

        # 투수 구성
        starters = sorted(
            [pitcher for pitcher in team["pitchers"]["starters"] if "선발" in pitcher["position"]],
            key=lambda x: x["stats"].get("ERA", float('inf'))
        )[:5]

        relievers = sorted(
            [
                pitcher for pitcher in team["pitchers"]["relievers"]
                if "불펜" in pitcher["position"] and pitcher not in starters
            ],
            key=lambda x: x["stats"].get("ERA", float('inf'))
        )[:6]

        if not relievers:
            print(f"경고: {team_name} 팀에 불펜 투수가 없습니다!")
        else:
            print(f"불펜 구성 완료: {[p['name'] for p in relievers]}")

        # AI 팀 이름 생성 및 데이터 저장
        ai_team_name = f"AI_team [{team_name}]"
        ai_teams[ai_team_name] = {
            "team_name": team_name,
            "batters": batters,
            "pitchers": {"starters": starters, "relievers": relievers},
        }

    return ai_teams


# --- 9이닝 시뮬레이션 ---
def calculate_probability(batter: Dict[str, Any], pitcher: Dict[str, Any], outcome_type: str, weather: str) -> float:
    # 날씨 효과 적용
    apply_weather_effects(batter, weather, is_batter=True)
    apply_weather_effects(pitcher, weather, is_batter=False)

    """타자와 투수의 대결 결과 확률 계산."""
    if outcome_type == "볼넷":
        return max(0, batter["stats"]["볼넷%"] * 0.2 + (11 + 2.5 * (pitcher["stats"]["볼넷/9"] - 4.2)))
    elif outcome_type == "삼진":
        return max(0, batter["stats"]["삼진%"] * 0.2 + (20 + 2.5 * (pitcher["stats"]["삼진/9"] - 7.2)))
    elif outcome_type == "안타":
        return max(0, batter["stats"]["타율"] * 100 + ((pitcher["stats"]["ERA"] - 4.8) * 0.06))
    elif outcome_type == "몸에 맞는 공":
        return 3  # 고정값
    elif outcome_type == "플라이 아웃":
        return max(0,0.5*(100 - ((batter["stats"]["타율"] * 100 + ((pitcher["stats"]["ERA"] - 4.8) * 0.06)) + (batter["stats"]["볼넷%"] * 0.2 + (11 + 2.5 * (pitcher["stats"]["볼넷/9"] - 4.2))) + (batter["stats"]["삼진%"] * 0.2 + (20 + 2.5 * (pitcher["stats"]["삼진/9"] - 7.2))))))
    elif outcome_type == "땅볼 아웃":
        return max(0,0.5*(100 - ((batter["stats"]["타율"] * 100 + ((pitcher["stats"]["ERA"] - 4.8) * 0.06)) + (batter["stats"]["볼넷%"] * 0.2 + (11 + 2.5 * (pitcher["stats"]["볼넷/9"] - 4.2))) + (batter["stats"]["삼진%"] * 0.2 + (20 + 2.5 * (pitcher["stats"]["삼진/9"] - 7.2))))))
    else:
        raise ValueError("Unknown outcome type.")
def determine_hit_type_direct(batter: Dict[str, Any]) -> str:
    """
    타자의 안타 개수를 기반으로 단타, 2루타, 3루타, 홈런 중 하나를 결정.
    """
    # 타자의 전체 안타 수
    total_hits = batter["stats"].get("안타", 0)

    # 전체 안타 수가 0인 경우 기본값 설정
    if total_hits == 0:
        return "단타"

    # 각 안타 유형의 개수
    single_hits = batter["stats"].get("단타", 0)
    double_hits = batter["stats"].get("2루타", 0)
    triple_hits = batter["stats"].get("3루타", 0)
    home_runs = batter["stats"].get("홈런", 0)

    # 확률 계산
    probabilities = {
        "단타": single_hits / total_hits,
        "2루타": double_hits / total_hits,
        "3루타": triple_hits / total_hits,
        "홈런": home_runs / total_hits,
    }

    # 결과 결정
    hit_types = list(probabilities.keys())
    weights = list(probabilities.values())
    hit_result = random.choices(hit_types, weights, k=1)[0]
    return hit_result
def calculate_out_probability(batter: Dict[str, Any], pitcher: Dict[str, Any]) -> Dict[str, float]:
    """
    땅볼 아웃과 플라이 아웃 확률을 계산합니다.
    """
    ground_out_prob = max(0, 50 + (pitcher["stats"]["ERA"] - 4.0) * 2 - batter["stats"]["타율"] * 50)
    fly_out_prob = max(0, 50 - (pitcher["stats"]["ERA"] - 4.0) * 2 + batter["stats"]["타율"] * 50)
    return {"ground_out": ground_out_prob, "fly_out": fly_out_prob}

def simulate_at_bat(batter: Dict[str, Any], pitcher: Dict[str, Any], weather: str) -> str:
    """
       타자와 투수의 대결에서 결과를 결정하며, 안타일 경우 단타/2루타/3루타/홈런을 추가로 결정.
       """
    outcomes = ["볼넷", "삼진", "안타", "몸에 맞는 공", "땅볼 아웃", "플라이 아웃"]
    probabilities = [
        calculate_probability(batter, pitcher, "볼넷", weather),
        calculate_probability(batter, pitcher, "삼진", weather),
        calculate_probability(batter, pitcher, "안타", weather),
        calculate_probability(batter, pitcher, "몸에 맞는 공", weather),
        calculate_probability(batter, pitcher, "플라이 아웃", weather),
        calculate_probability(batter, pitcher, "땅볼 아웃", weather),

    ]

    # 확률 합 정규화
    total = sum(probabilities)
    normalized_probabilities = [p / total * 100 for p in probabilities]
    result = random.choices(outcomes, normalized_probabilities, k=1)[0]

    # 안타일 경우, 추가로 단타/2루타/3루타/홈런 결정
    if result == "안타":
        hit_type = determine_hit_type_direct(batter)
        return hit_type

    return result

def simulate_inning(batting_team: List[Dict[str, Any]], pitching_team: List[Dict[str, Any]], inning_number: int, weather: str) -> int:
    """이닝 시뮬레이션."""
    outs = 0
    score = 0
    bases = [None, None, None]  # 1루, 2루, 3루 상태 저장
    # 투수 선택
    if inning_number <= 5:
        # 선발 투수: 1~5 이닝
        pitcher = pitching_team["starters"][(inning_number - 1) % len(pitching_team["starters"])]
    else:
        #불펜 투수: 6이닝~
        pitcher = pitching_team["relievers"][(inning_number - 1) % len(pitching_team["relievers"])]

    print(f"\n투수: {pitcher['name']} | 경기 날씨: {weather} | 투수 선호 날씨: {pitcher['weather']}")

    for batter in batting_team:
        if outs >= 3:
            break

        # 날씨 효과 적용
        apply_weather_effects(batter, weather, is_batter=True)  # 타자 스탯 조정
        apply_weather_effects(pitcher, weather, is_batter=False)  # 투수 스탯 조정


        print(f"타석: 타자 {batter['name']} vs 투수 {pitcher['name']}")
        result = simulate_at_bat(batter, pitcher,weather)

        if result == "플라이 아웃":
            # 희생플라이 처리
            score += handle_tag_up(bases, outs)
            outs += 1
            print(f"결과: {batter['name']} 플라이 아웃! 현재 아웃 카운트: {outs}")
        if result == "땅볼 아웃":
            # 희생타 처리
            additional_score, outs = handle_ground_out(bases, outs)
            score += additional_score
            print(f"결과: {batter['name']} 땅볼 아웃! 현재 아웃 카운트: {outs}")
        elif result == "삼진":
            outs += 1
            print(f"결과: {batter['name']} 헛스윙 삼진아웃! 현재 아웃 카운트: {outs}")
        elif result == "몸에 맞는 공":
            print(f"결과: {batter['name']} 몸에 맞는 공! 타자 1루 진루.")
            score += handle_walk_or_hit_by_pitch(bases)
        elif result == "볼넷":
            print(f"결과: {batter['name']} 볼넷! 주자 1루 진루.")
            score += handle_walk_or_hit_by_pitch(bases)
            bases[0] = batter['name']  # 타자가 1루로 이동
        elif result in ["단타", "2루타", "3루타", "홈런"]:
            print(f"결과: {batter['name']} {result}!")
            if result == "단타":
                score += advance_runner(bases, 1)  # 모든 주자 1베이스 이동
                bases[0] = batter["name"]  # 타자 1루로 이동
            elif result == "2루타":
                score += advance_runner(bases, 2)  # 모든 주자 2베이스 이동
                bases[1] = batter["name"]  # 타자 2루로 이동
            elif result == "3루타":
                score += advance_runner(bases, 3)  # 모든 주자 3베이스 이동
                bases[2] = batter["name"]  # 타자 3루로 이동
            elif result == "홈런":
                score += sum(1 for b in bases if b) + 1  # 모든 주자와 타자 득점
                bases = [None, None, None]  # 베이스 초기화
            #print(f"현재 베이스 상태: {bases}")
        # 현재 베이스 상태 출력
        base_state = [f"{base if base else '주자없음'}" for base in bases]
        print(f"현재 베이스 상태: {base_state}")

    print(f"이닝 종료: 득점 {score}점")
    return score


def advance_runner(bases: List[bool], steps: int):

    """
           주자를 이동시키고 점수를 계산합니다.
           :param bases: 현재 베이스 상태 (1루, 2루, 3루).
           :param hit: 타자의 안타 타입 (1: 단타, 2: 2루타, 3: 3루타, 4: 홈런).
           :return: 득점한 점수.
           """
    score = 0
    for i in range(2, -1, -1):  # 3루에서 1루 방향으로 이동
        if bases[i]:
            if i + steps >= 3:  # 홈 도달 시 주자를 홈으로
                print(f"{bases[i]} 홈 도착! 점수 추가!")
                bases[i] = None
            else:
                bases[i + steps] = bases[i]
                bases[i] = None
    if steps < 4:
        bases[steps - 1] = "타자"
    return score
def handle_walk_or_hit_by_pitch(bases: List[Any]) -> int:
    """
    볼넷 또는 몸에 맞는 공 발생 시 주자와 타자 이동을 처리하고 득점을 계산합니다.
    :param bases: 현재 베이스 상태 (1루, 2루, 3루).
    :return: 득점한 점수.
    """
    score = 0

    # 3루에서 1루 방향으로 이동
    for i in range(2, -1, -1):
        if bases[i]:  # 해당 베이스에 주자가 있으면
            if i == 2:  # 3루 주자는 홈으로 들어감
                score += 1
                print(f"{bases[i]} 홈 도착! 점수 추가!")
                bases[i] = None  # 3루 비우기
            else:
                # 주자를 한 베이스 앞으로 이동
                bases[i + 1] = bases[i]
                bases[i] = None  # 이전 베이스 비우기

    # 타자를 1루로 이동
    bases[0] = "타자"

    return score
def handle_tag_up(bases: List[Any], outs: int) -> int:
    """
    태그업 상황에서 3루 주자가 득점하는 로직.
    :param bases: 현재 베이스 상태.
    :param outs: 현재 아웃 수.
    :return: 득점한 점수 (0 또는 1).
    """
    if outs < 2 and bases[2]:  # 태그업 조건: 3루 주자 있고, 0 또는 1아웃
        print(f"{bases[2]} 3루 주자가 홈 도착! 점수 추가!")
        bases[2] = None  # 3루 비우기
        return 1  # 점수 1점 추가
    return 0
def handle_ground_out(bases: List[Any], outs: int) -> (int, int):
    """
    땅볼 아웃 처리.
    :param bases: 현재 베이스 상태.
    :param outs: 현재 아웃 수.
    :return: 득점한 점수 (0 또는 1)와 업데이트된 아웃 수.
    """
    score = 0

    if outs < 2:  # 0아웃 또는 1아웃일 때
        if bases[2] and bases[0]:  # 3루 주자와 1루 주자가 동시에 있을 경우
            if outs == 0:  # 0아웃일 경우 득점 인정 1아웃일 경우 득점 인정 X
                print(f"{bases[2]} 3루 주자가 득점! 희생타점 올렸습니다.")
                score += 1
                bases[2] = None
                print(f"{bases[0]} 1루 주자가 병살 처리로 아웃되었습니다.")
                bases[0] = None
                outs += 2
            else:  # 1아웃일 경우 득점 불인정
                print(f"{bases[2]} 3루 주자가 홈으로 진루하지 못했습니다.")
                print(f"{bases[0]} 1루 주자가 병살 처리로 아웃되었습니다.")
                bases[0] = None
                outs += 2
        elif bases[2] and bases[1] and bases[0]:  # 3루 주자, 2루 주자 ,1루 주자가 동시에 있을 경우
            if outs == 0:  # 0아웃일 경우 득점 인정 1아웃일 경우 득점 인정 X
                print(f"{bases[2]} 3루 주자가 득점! 희생타점 올렸습니다.")
                score += 1
                bases[2] = None
                print(f"{bases[0]} 1루 주자가 병살 처리로 아웃되었습니다.")
                bases[0] = None
                outs += 2
            else:  # 1아웃일 경우 득점 불인정
                print(f"{bases[2]} 3루 주자가 홈으로 진루하지 못했습니다.")
                print(f"{bases[0]} 1루 주자가 병살 처리로 아웃되었습니다.")
                bases[0] = None
                outs += 2
        elif bases[2] and bases[1] :  # 3루 주자와 2루 주자가 동시에 있을 경우
            print(f"{bases[2]} 3루 주자가 득점! 희생타점 올렸습니다.")
            bases[2] = None
            score += 1
            outs += 1
        elif bases[2] and bases[0]:  # 2루 주자와 1루 주자가 동시에 있을 경우
            print(f"{bases[0]} 1루 주자가 병살 처리로 아웃되었습니다.")
            bases[0] = None
            outs += 2
        elif bases[2]:  # 3루 주자만 있을 경우
            print(f"{bases[2]} 3루 주자가 득점! 희생타점 올렸습니다.")
            bases[2] = None
            score += 1
            outs += 1
        elif bases[1]:  # 2루 주자만 있을 경우
            print(f"{bases[1]} 2루 주자는 진루하지 못했습니다.")
            outs += 1  # 2루 주자 처리 없이 아웃만 증가
        elif bases[0]:  # 1루 주자만 있을 경우
            print(f"{bases[0]} 1루 주자가  병살 처리되어 아웃되었습니다.")
            bases[0] = None
            outs += 2
        else:
            outs += 1

    else:  # 2아웃일 때  # 타자만 처리
        outs += 1

    return score, outs

def get_random_weather() -> str:
    """
    랜덤하게 경기장의 날씨를 반환.
    """
    weather_options = ["맑음", "흐림", "비옴", "눈옴"]  # 날씨 옵션
    return random.choice(weather_options)

def apply_weather_effects(player: Dict[str, Any], weather: str, is_batter: bool = True):
    """
    선수의 날씨 선호에 따른 스탯 조정.
    :param player: 선수 데이터 (타자 또는 투수)
    :param weather: 현재 경기장의 날씨
    :param is_batter: 타자인지 여부 (True: 타자, False: 투수)
    """
    if player["weather"] == weather:  # 선호하는 날씨와 일치할 경우
        if is_batter:
            player["stats"]["볼넷%"] *= 0.9
            player["stats"]["삼진%"] *= 0.9
            player["stats"]["타율"] *= 1.2
        else:
            player["stats"]["볼넷/9"] *= 0.9
            player["stats"]["삼진/9"] *= 1.2
            player["stats"]["ERA"] *= 0.9

def simulate_game(team1: Dict[str, Any], team2: Dict[str, Any],weather: str) -> None:
    """팀1과 팀2의 9이닝 게임을 시뮬레이션하고 경기 과정을 출력."""
    score_team1 = 0
    score_team2 = 0

    # 경기 시작: 선발 명단 출력
    print("\n--- 경기 시작 ---")
    print(f"팀1: {team1['team_name']}")
    print_batter_list_by_position(team1["batters"])
    print_selected_pitchers(team1["pitchers"]["starters"], team1["pitchers"]["relievers"])  # 팀1 투수 출력



    print(f"\n팀2: {team2['team_name']}")
    print_batter_list_by_position(team2["batters"])
    print_selected_pitchers(team2["pitchers"]["starters"], team2["pitchers"]["relievers"])  # 팀2 투수 출력


    # 9이닝 시뮬레이션
    for inning in range(1, 10):
            print(f"\n--- {inning}회초 ---")
            score_team1 += simulate_inning(team1["batters"], team2["pitchers"], inning, weather)
            print(f"\n--- {inning}회말 ---")
            score_team2 += simulate_inning(team2["batters"], team1["pitchers"], inning, weather)

    # 최종 결과 출력
    print("\n--- 경기 종료 ---")
    print(f"{team1['team_name']} {score_team1} : {score_team2} {team2['team_name']}")
    if score_team1 > score_team2:
        print(f"{team1['team_name']} 승리!")
    elif score_team1 < score_team2:
        print(f"{team2['team_name']} 승리!")
    else:
        print("무승부!")

# --- 메인 ---
if __name__ == "__main__":
    pitcher_file = r"C:\Users\u\Desktop\KBO_시뮬\KBO 2024 투수 종합지표.xlsx"
    batter_file = r"C:\Users\u\Desktop\KBO_시뮬\KBO2024 타자 종합지표.xlsx"

    pitchers = load_pitcher_data(pitcher_file)
    batters = load_batter_data(batter_file)
    team_data = group_by_team(pitchers, batters)

    # 유저 팀 구성
    user_team = select_user_team(team_data)

    # 나머지 구단 자동 구성
    ai_teams = auto_configure_teams(team_data, user_team["team_name"])

    # 모든 팀 데이터 통합
    all_teams = {user_team["team_name"]: user_team, **ai_teams}

    # 상대 팀 선택
    opponent_team_name = random.choice(list(ai_teams.keys()))
    opponent_team = ai_teams[opponent_team_name]

    # 구장 날씨 랜덤 설정
    stadium_weather = get_random_weather()
    print(f"오늘의 경기 날씨: {stadium_weather}")

    # 게임 실행
    simulate_game(user_team, opponent_team, stadium_weather)

