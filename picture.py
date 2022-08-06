# def getUserIDfromNAME(user_name):
#     """
#     나 여긴 뭐가 뭔지 모름 너가 함수 만드샘
#     """
#     return ctx.name
    
# def refine_txt(target_file,split_unit='$',name_index=0) -> None:
#     with open(target_file,'r') as before:
#         temp = before.read().split('\n')
#         for e in temp:
#             replacement = f'{e}{split_unit}{getUserIDfromNAME(e[name_index])}'
#             rewrite_txt(target_file,e,replacement=replacement)
#     return None



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

@bot.command()
async def 소환(ctx):
    """
    # dataform   -   사진이름$URL$유저이름$유저아이디
    """
    
    # log 저장
    with open(log_file_name, "a") as file:
        file.write(str(datetime.datetime.now()) + ctx.message.content + " " + ctx.author.name + " " + str(ctx.author.guild) + "\n")
    
    # 내부 변수
    SPAWN_FILE = picture_log
    RESERVED = ('정보', '저장', '명령어', '삭제', '이름변경')

    class USER_:
        def __init__(self ,name = '', channel = '', input = []) -> None:
            class command:
                def __init__(self, detail = '', spawnName = '', newName = '', saveName = '') -> None:
                    self.detail = detail # ∈ RESERVED  /  '*소환'의 세부 명령어   
                    self.spawnName = spawnName # [(이름]
                    self.newName = newName # [바꿀이름]
            self.NAME = name
            self.CHANNEL = channel
            self.INPUT = input
            self.command = command()

    USER_INPUT = ctx.message.content.replace('*소환','').split()
    # USER_INPUT = ctx.message.content.split()[1:]
    discordUSER = USER_(ctx.author, ctx.channel, USER_INPUT)


    if len(USER_INPUT) == 1 and not(discordUSER.INPUT[0] in RESERVED): # *소환 [이름]
        discordUSER.command.detail = '소환'
        discordUSER.command.spawnName = discordUSER.INPUT[0]

    elif len(USER_INPUT) == 1 and discordUSER.INPUT[0] == '정보': # *소환 정보
        discordUSER.command.detail = '정보'
    
    elif len(USER_INPUT) == 1 and discordUSER.INPUT[0] == '명령어': # *소환 명령어
        discordUSER.command.detail = '명령어'

    elif len(USER_INPUT) == 2 and discordUSER.INPUT[0] == '저장': # *소환 저장 [이름]
        discordUSER.command.detail = '저장'
        discordUSER.command.spawnName = discordUSER.INPUT[1]

    elif len(USER_INPUT) == 2 and discordUSER.INPUT[0] == '삭제': # *소환 삭제 [이름]
        discordUSER.command.detail = '삭제'
        discordUSER.command.spawnName = discordUSER.INPUT[1]

    elif len(USER_INPUT) == 3 and discordUSER.INPUT[0] == '이름변경': # *소환 이름변경 [이름] [바꿀이름]
        discordUSER.command.detail = '이름변경'
        discordUSER.command.spawnName = discordUSER.INPUT[1]
        discordUSER.command.newName = discordUSER.INPUT[2]
    
    else:
        await ctx.send("잘못된 입력입니다. ( `*소환 명령어`  참고 ) ")

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 0.0/M    ] --')
        return None
        #######################################
        #


    if discordUSER.command.detail == '소환': # *소환 [이름]
        with open(SPAWN_FILE, "r") as file:
            # lines = file.readlines()
            for line in file.readlines():
                if discordUSER.command.spawnName == line.split("$")[0]:
                    url = line.split("$")[1]
        
        if url == "":
            await ctx.send("||없는딩?||")

        else:
            embed = discord.Embed(title=discordUSER.command.spawnName , color=ctx.author.color)
            embed.set_image(url=url) # 이미지의 링크를 지정해 이미지를 설정합니다.
            await ctx.send(embed=embed) # 메시지를 보냅니다.

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.0/M    ] --')
        return None
        #######################################
        #


    elif discordUSER.command.detail == '정보': # *소환 정보
        with open(SPAWN_FILE, "r") as file:
            text = ""
            # lines = file.readlines()
            for l in file.readlines():
                text = text + l.split("$")[0] + " / " + l.split("$")[2]
            await ctx.send(f"```{text}```")
        
        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.1/M    ] --')
        return None
        #######################################
        #


    elif discordUSER.command.detail == '명령어': # *소환 명령어
        await ctx.send(
            """
            ```
            *소환 [NAME]
                정보
                명령어
                저장 [NAME]
                삭제 [NAME]
                이름변경 [NAME] [newNAME]
            ```
            """
        )

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.2/M    ] --')
        return None
        #######################################
        #


    elif discordUSER.command.detail == '저장': # *소환 저장 [이름]
        save_name = discordUSER.command.spawnName
        
        #예약어가 쓰였는지 확인
        if save_name in RESERVED:
            await ctx.send(
                f"""'{save_name}'(이)라는 이름으로 사진을 저장할 수 없습니다.
                그 외 {RESERVED}"""
            )
            #######################################
            print('<CONSOLE DEBUG> -- [    소환 EOP - 1.3/0    ] --')
            return None
            #######################################

        #이미 있는 파일인지 확인
        if file_Overlap(save_name,SPAWN_FILE,strict_inspection=0):
            await ctx.send("중복임 ㅇㅇ")
            #######################################
            print('<CONSOLE DEBUG> -- [    소환 EOP - 1.3/1    ] --')
            return None
            #######################################

        #파일에 추가하기.
        with open(SPAWN_FILE, "a") as file:
            IMG = some_USER_INPUT(discordUSER.NAME, discordUSER.CHANNEL)
            # DATA FORM ###################################################################################
            file.write(f"{save_name}${IMG.attachments[0].url}${str(discordUSER.NAME.name)}${str(discordUSER.NAME.id)}\n")
            # 사진이름$URL$유저이름$유저아이디\n #################################################################
            print('<CONSOLE DEBUG> -- [    SPAWN_FILE OPENED    ] --')
        
        await ctx.send(
            f"""사진을 **{save_name}**로 저장완료
            사진을 삭제하지 말아주세요"""
        )

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.3/M    ] --')
        return None
        #######################################
        #

    elif discordUSER.command.detail == '삭제': # *소환 삭제 [이름]

        delete_picture = False
        with open(SPAWN_FILE, "r") as file:
            # lines = file.readlines()
            for line in file.readlines():
                if line.split("$")[0] == discordUSER.command.spawnName:
                    if line.split("$")[3] == discordUSER.NAME.id:
                        delete_picture = True

                    else:
                        picture_owner=line.split("$")[2]
                        await ctx.send(f"**{discordUSER.command.spawnName}**을 저장한 ***{picture_owner}***만 삭제할 수 있습니다.")
                        #######################################
                        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.4/0    ] --')
                        return None
                        #######################################

                else:
                    await ctx.send("응 없어")
                    #######################################
                    print('<CONSOLE DEBUG> -- [    소환 EOP - 1.4/1    ] --')
                    return None
                    #######################################

        await ctx.send("정말로 삭제하려면 `yes!` 라고 입력해주세요. (10초 안에 입력)")
        delete_truly = True if some_USER_INPUT(discordUSER.NAME, discordUSER.CHANNEL,timeOut=10) == 'yes!' else False
        
        if delete_picture and delete_truly:
            rewrite_txt(SPAWN_FILE,discordUSER.command.spawnName,"")
            await ctx.send("삭제 완료")

        else:
            await ctx.send("삭제 실패, 다시시도 해주세요.")

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.4/M    ] --')
        return None
        #######################################
        #


    elif discordUSER.command.detail == '이름변경': # *소환 이름변경 [이름] [바꿀이름]
        save_name = discordUSER.command.spawnName
        new_name = discordUSER.command.newName
        #예약어가 쓰였는지 확인
        if new_name in RESERVED:
            await ctx.send(
                f"""'{new_name}'(이)라는 이름으로 사진을 저장할 수 없습니다.
                그 외 {RESERVED}"""
            )
            #######################################
            print('<CONSOLE DEBUG> -- [    소환 EOP - 1.5/0    ] --')
            return None
            #######################################

        #이름변경하는 사람이 등록한 사람인지 확인
        with open(SPAWN_FILE, "r") as file:
            # lines = file.readlines()
            for line in file.readlines():
                if line.split("$")[0] == discordUSER.command.spawnName:
                    origin = line.split("$")

                    if origin[3] != discordUSER.NAME.id:

                        picture_owner=origin[2]
                        
                        await ctx.send(f"**{discordUSER.command.spawnName}**을 저장한 ***{picture_owner}***만 이름변경을 할 수 있습니다.")
                        #######################################
                        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.5/1    ] --')
                        return None
                        #######################################

                else:
                    await ctx.send(f"{discordUSER.command.spawnName} 같은 건 없다.")
                    #######################################
                    print('<CONSOLE DEBUG> -- [    소환 EOP - 1.5/2    ] --')
                    return None
                    #######################################

        replacement = f'{new_name}${origin[1]}${origin[2]}${origin[3]}'
        rewrite_txt(SPAWN_FILE,save_name,replacement=replacement)

        await ctx.send(f'사진 {save_name}을(를) {new_name}(으)로 바꾸어 저장함.')

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.5/M    ] --')
        return None
        #######################################
        #