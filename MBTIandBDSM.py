import extend_func as exFunc

async def mbti(ctx):
    # LOG 생성
    with open(log_file_name, "a") as file:
        file.write(str(datetime.datetime.now()) + ctx.message.content + " " + ctx.author.name + " " + str(ctx.author.guild) + "\n")

    # 내부 변수
    mbti_file = "MBTIs.txt"
    changePrefix = ('변경', '바꾸기', 'change', 'c', 'reset')
    changeMBTI = False
    
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
        exFunc.rewrite_txt(mbti_file, ctx.author.name, data)
        print(f"<DEBUG> 다시쓰기 '{mbti_file}'")
        return

    # *mbti [MBTI]
    with open(mbti_file, "a") as file:
        file.write(data) 
        print(f"<DEBUG> 쓰기 '{mbti_file}'")
    
    # EOP
    isSaved = f"""{str(ctx.author.name)}의 MBTI를 **{mbti_type}** 로 저장완료"""
    await ctx.send(isSaved) 


@bot.command(help = "*저장 저장할이름 입력후 사진을 보내면됩니다.")
async def bdsm(ctx, bdsm_linked_picture):
    # LOG 생성
    with open(log_file_name, "a") as f:
        f.write(str(datetime.datetime.now()) + ctx.message.content + " " + ctx.author.name + " " + str(ctx.author.guild) + "\n")
    
    channel = ctx.channel 
    
    # BDSM_LINKED_PICTURE FILE OPEN (with 중복시 넘김)
    with open(bdsm_links, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.split("$")[0] == bdsm_linked_picture:
                await ctx.send("중복")
                return
    
    # CHECK ALL USER MSG "WHILE" REQUESTED USER MSG
    user_command = ''
    def check(user_msg):
        print(f"<DEBUG> CHECK '{user_msg}' ")
        return user_msg.author == ctx.author and user_msg.channel == ctx.channel and not user_msg.attachments[0].url == "404" 
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=100.0)
    except asyncio.TimeoutError:
        await channel.send(f"***{user_command}***의 저장 시간 초과")
    
    # BDSM_LINKED_PICTURE FILE WRITE
    with open(bdsm_links, "a") as f:
        f.write(bdsm_linked_picture+"$"+msg.attachments[0].url + "$" + str(ctx.author.name) + "\n") 
        print("<DEBUG> OPENED 'bdsm_links'")

    isSaved = f"""사진을 **{bdsm_linked_picture}** 로 저장완료
    사진을 삭제하지 말아주세요"""
    await ctx.send(isSaved)