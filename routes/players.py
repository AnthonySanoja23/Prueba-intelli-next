import xlsxwriter
import io
import datetime

from fastapi import APIRouter
from config.db import conn
from models.players import players
from schemas.players import Player
from typing import List
from data_set.data_set import get_players_api
from fastapi.responses import StreamingResponse


player = APIRouter()


@player.get(
    "/players",
    tags=["players"],
    response_model=List[Player],
    description="Get a list of all Players",
    response_description='xlsx',
)
def get_players():
    allplayers = get_players_api()
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    rows = 1
    is_created = False
    
    for idx, player in enumerate(allplayers):
        dict_player = dict(player)
        
        if is_created:
            columns=0
            for key, value in dict_player.items():
                worksheet.write(rows, columns,value)
                columns+=1
        else:
            columns = 0
            for key, value in dict_player.items(): 
                worksheet.write(0, columns,key)
                worksheet.write(rows, columns,value)
                columns+=1
                is_created = True
        rows+=1
        
    workbook.close()
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="players.xlsx"'
    }
    return StreamingResponse(output, headers=headers)
    