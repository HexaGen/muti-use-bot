def mbti_to_img(mbti) -> str('LINK'):
    # 픽셀이미지 아니고 벡터이미지 임
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

def rewrite_txt(target_file, current_data, replacement) -> None:
    # current_data : target_file에서 USER_NAME과 같은 카테고리로 가져오는 것이 가능함. 
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
    except:
        print(f"원본({target_file})에 바꾸려는 데이터({current_data})가 없습니다.")
        return None
    
    # 새로 쓰기
    with open(target_file, 'w') as after:
        after.writelines('\n'.join(temp))
        return None

async def mbti(ctx):
    # LOG 생성
    with open(log_file_name, "a") as file:
        file.write(str(datetime.datetime.now()) + ctx.message.content + " " + ctx.author.name + " " + str(ctx.author.guild) + "\n")

    # 내부 변수
    mbti_file = "MBTIs.txt"
    changeMBTI = False
    changePrefix = ('변경', '바꾸기', 'change', 'c', 'reset')
    
    # 명령어 인식
    user_msg = ctx.message.content.replace('*mbti','').split()
    if len(user_msg) == 1:
        mbti_type = user_msg[0]
    elif len(user_msg) == 2 and user_msg[0] in changePrefix :
        mbti_type = user_msg[1]
        changeMBTI = True
    else:
        isError_command = f"""정확하게 명령어를 입력해주세요!
        `*mbti (MBTI)` 혹은
        `*mbti {changePrefix[0]}{changePrefix[1:]} (MBTI)` 입니다."""
        await ctx.send(isError_command)
    
    #데이터 형식 "[이름]$[MBTI]"
    data = f"{ctx.author.name}${mbti_type}"

    # *mbti 변경 [MBTI]
    if changeMBTI:
        rewrite_txt(mbti_file, ctx.author.name, data)
        print(f"<DEBUG> 다시쓰기 '{mbti_file}'")
        return

    # *mbti [MBTI]
    with open(mbti_file, "a") as file:
        file.write(data) 
        print(f"<DEBUG> 쓰기 '{mbti_file}'")
    
    # EOP
    isSaved = f"""{str(ctx.author.name)}의 MBTI를 **{mbti_type}** 로 저장완료"""
    await ctx.send(isSaved) 