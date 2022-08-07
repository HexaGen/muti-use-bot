import extend_func as exFunc

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
        if exFunc.file_Overlap(save_name,SPAWN_FILE,strict_inspection=0):
            await ctx.send("중복임 ㅇㅇ")
            #######################################
            print('<CONSOLE DEBUG> -- [    소환 EOP - 1.3/1    ] --')
            return None
            #######################################

        #파일에 추가하기.
        with open(SPAWN_FILE, "a") as file:
            IMG = exFunc.some_USER_INPUT(discordUSER.NAME, discordUSER.CHANNEL)
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
        delete_truly = True if exFunc.some_USER_INPUT(discordUSER.NAME, discordUSER.CHANNEL,timeOut=10) == 'yes!' else False
        
        if delete_picture and delete_truly:
            exFunc.rewrite_txt(SPAWN_FILE,discordUSER.command.spawnName,"")
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
        exFunc.rewrite_txt(SPAWN_FILE,save_name,replacement=replacement)

        await ctx.send(f'사진 {save_name}을(를) {new_name}(으)로 바꾸어 저장함.')

        #######################################
        print('<CONSOLE DEBUG> -- [    소환 EOP - 1.5/M    ] --')
        return None
        #######################################
        #