def rewrite_txt(target_file, current_data, replacement) -> None:
    """
    current_data : target_file에서 USER_NAME과 같은 카테고리로 가져오는 것이 가능함.
    - 'replacement'가 NULL('', False, 0) 이면 'current_data'를 지워버림
    """
    # 원본 복사
    temp = []
    with open(target_file, 'r') as before:
        temp = before.read().split('\n')
    
    # 원본에서 current_data 찾기
    try:
        i=0
        for element in temp:
            if current_data in element:
                break
            i += 1
        temp[i] = replacement
        try:
            if not replacement:
                temp.pop(i)
        except:
            print("NULL인 CELL을 뽑아내지 못함.")    
    except:
        print(f'<CONSOLE DEBUG> -- [    rewrite_txt EOP - 0.0    |    ({target_file}, {current_data}, {replacement})    ] --')
        print(f"원본({target_file})에 바꾸려는 데이터({current_data})가 없습니다.")
        return None
    
    # 새로 쓰기
    with open(target_file, 'w') as after:
        after.writelines('\n'.join(temp))
        print(f'<CONSOLE DEBUG> -- [    rewrite_txt EOP - 1.0    |    ({target_file}, {current_data}, {replacement})    ] --')
        return None


async def some_USER_INPUT(targetUser, targetChannel, timeOut = 100) -> str or False:
    """
    ## 특정'CHANNEL'에서 특정'USER'의 'USER_INPUT'만 받아오는 함수
    check()함수는 알아서 지지고볶
    """
    # 내부 변수
    TARGETED_MSG = ''

    def check(any_user_message):
        return (
            any_user_message.author == targetUser and
            any_user_message.channel == targetChannel and
            not any_user_message.attachments[0].url == "404"
        )

    try:
        TARGETED_MSG = await bot.wait_for("message", check=check, timeout=timeOut)
    except asyncio.TimeoutError:
        await targetChannel.send(f"입력시간({int(timeOut)}초) 초과")
        return False

    print(f'<CONSOLE DEBUG> -- [    some_USER_INPUT EOP - 0.0    |    ({targetUser}, {targetChannel}, {timeOut})    ] --')
    return TARGETED_MSG


def file_Overlap(input_data, target_file, strict_inspection = '', split_unit='$') -> bool:
    """
    ## 중복 확인 함수
    'input_data'가 'target_file'에 존재하는지 확인 한다.
    'strict_inspection'이 'None'이면 엄밀한 검사를 하지 않는다.
    - 엄밀한 검사는 'target_file'에서 'data_split_unit'으로 나누어져 만들어지는 *리스트(list)*에서
    'strict_inspection'번째 인덱스에 'input_data'가 있는지 확인 하는 것이다.
      - 즉, target_file.split(data_split_unit)[strict_inspection] == input_data
    """
    if not str(strict_inspection).isdigit():    
        with open(target_file, "r") as file:
            # lines file.readlines():
            for line in file.readlines():
                if input_data in line:
                    print(f'<CONSOLE DEBUG> -- [    file_Overlap EOP - 0.0    |    {input_data}는 이미 {target_file}에 있습니다.    ] --')
                    return True
    else:
        with open(target_file, "r") as file:
            # lines file.readlines():
            for line in file.readlines():
                if line.split(split_unit)[strict_inspection] == input_data:
                    print(f'<CONSOLE DEBUG> -- [    file_Overlap EOP - 0.1    |    {input_data}는 이미 {target_file}에 있습니다.    ] --')
                    return True

    # await ctx.send("중복")
    print(f'<CONSOLE DEBUG> -- [    file_Overlap EOP - 1.0    |    ({input_data}, {target_file}, {strict_inspection}, {data_split_unit})    ] --')
    return False


def mbti_to_img(mbti) -> str('LINK'):
    mbti_img = {
        'INTJ': 'https://static.neris-assets.com/images/personality-types/headers/analysts_Architect_INTJ_personality_header.svg',
        'INTP': 'https://static.neris-assets.com/images/personality-types/headers/analysts_Logician_INTP_personality_header.svg',
        'ENTJ': 'https://static.neris-assets.com/images/personality-types/headers/analysts_Commander_ENTJ_personality_header.svg',
        'ENTP': 'https://static.neris-assets.com/images/personality-types/headers/analysts_Debater_ENTP_personality_header.svg',
        'INFJ': 'https://static.neris-assets.com/images/personality-types/headers/diplomats_Advocate_INFJ_personality_header.svg',
        'INFP': 'https://static.neris-assets.com/images/personality-types/headers/diplomats_Mediator_INFP_personality_header.svg',
        'ENFJ': 'https://static.neris-assets.com/images/personality-types/headers/diplomats_Protagonist_ENFJ_personality_header.svg',
        'ENFP': 'https://static.neris-assets.com/images/personality-types/headers/diplomats_Campaigner_ENFP_personality_header.svg',
        'ISTJ': 'https://static.neris-assets.com/images/personality-types/headers/sentinels_Logistician_ISTJ_personality_header.svg',
        'ISFJ': 'https://static.neris-assets.com/images/personality-types/headers/sentinels_Defender_ISFJ_personality_header.svg',
        'ESTJ': 'https://static.neris-assets.com/images/personality-types/headers/sentinels_Executive_ESTJ_personality_header.svg',
        'ESFJ': 'https://static.neris-assets.com/images/personality-types/headers/sentinels_Consul_ESFJ_personality_header.svg',
        'ISTP': 'https://static.neris-assets.com/images/personality-types/headers/explorers_Virtuoso_ISTP_personality_header.svg',
        'ISFP': 'https://static.neris-assets.com/images/personality-types/headers/explorers_Adventurer_ISFP_personality_header.svg',
        'ESTP': 'https://static.neris-assets.com/images/personality-types/headers/explorers_Entrepreneur_ESTP_personality_header.svg',
        'ESFP': 'https://static.neris-assets.com/images/personality-types/headers/explorers_Entertainer_ESFP_personality_header.svg'
    }

    return mbti_img[mbti]