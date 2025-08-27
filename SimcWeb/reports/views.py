from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib import colors
from datetime import datetime
from medicao.models import Medicao
from zoneinfo import ZoneInfo
from SimcWeb.context_processors import localizacao


def gerar_relatorio(request):
    
    # Obtém as informações de localização diretamente
    dados_localizacao = localizacao(request)
    tz = ZoneInfo(dados_localizacao["timezone"])

    # --- 1. Recebe filtros do formulário ---
    data_inicial = request.GET.get("data_inicial")
    data_final = request.GET.get("data_final")
    hora_inicial = request.GET.get("hora_inicial")
    hora_final = request.GET.get("hora_final")
    campos = request.GET.getlist("campos")  # lista de campos escolhidos (checkbox)

    # Monta datetime inicial/final
    dt_inicio_str = f"{data_inicial} {hora_inicial}" if data_inicial and hora_inicial else data_inicial
    dt_fim_str = f"{data_final} {hora_final}" if data_final and hora_final else data_final
    if dt_inicio_str:
        dt_inicio = parse_datetime(dt_inicio_str)
    if dt_inicio.tzinfo is None:
        dt_inicio = dt_inicio.replace(tzinfo=tz)
    else:
        dt_inicio = None

    if dt_fim_str:
        dt_fim = parse_datetime(dt_fim_str)
    if dt_fim.tzinfo is None:
        dt_fim = dt_fim.replace(tzinfo=tz)
    else:
        dt_fim = None


    # Consulta ao banco de dados
    qs = Medicao.objects.all()
    if dt_inicio:
        qs = qs.filter(data_hora__gte=dt_inicio)
    if dt_fim:
        qs = qs.filter(data_hora__lte=dt_fim)

    qs = qs.order_by("data_hora")

    # --- 2. Prepara resposta HTTP PDF ---
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Relatório SIMC.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()
    elementos = []

    # --- 3. Cabeçalho com logo ---
    logo = "static/img/logo-azul.png"  # coloque o caminho correto do seu logo
    elementos.append(Image(logo, width=140, height=45))
    elementos.append(Spacer(1, 12))

    titulo_style = ParagraphStyle(
        name="Titulo",
        fontSize=18,
        alignment=1,
        spaceAfter=25,
        textColor=colors.HexColor("#004b9b"),
        fontName="Helvetica-Bold"
    )
    elementos.append(Paragraph("Relatório de Monitoramento Climático", titulo_style))
    elementos.append(HRFlowable(color=colors.HexColor("#004b9b"), thickness=1.2, width="100%"))
    elementos.append(Spacer(1, 20))

    # --- 4. Informações dos filtros aplicados ---
    labels = {
        "temperatura": "Temperatura",
        "umidade_ar": "Umidade do Ar",
        "chuva": "Chuva",
        "luminosidade": "Luminosidade",
        "umidade_solo": "Umidade do Solo",
        "uv": "Índice UV"
    }

    campos_formatados = ", ".join(labels.get(c, c).title() for c in campos)
    data_inicial_fmt = dt_inicio.astimezone(tz).strftime("%d/%m/%Y - %H:%M") if dt_inicio else "-"
    data_final_fmt = dt_fim.astimezone(tz).strftime("%d/%m/%Y - %H:%M") if dt_fim else "-"

    filtros_texto = f"""
    <b>Período:</b> {data_inicial_fmt} até {data_final_fmt}<br/>
    <b>Dados Selecionados:</b> {campos_formatados}
    """
    elementos.append(Paragraph(filtros_texto, styles["Normal"]))
    elementos.append(Spacer(1, 18))

    # --- 5. Monta tabela dinamicamente ---
    cabecalho = ["Data/Hora"] + [labels.get(c, c).title() for c in campos]
    tabela_dados = [cabecalho]

    for med in qs:
        linha = [med.data_hora.astimezone(tz).strftime("%d/%m/%Y %H:%M")]
        for campo in campos:
            valor = getattr(med, campo.lower().replace(" ", "_"), None)
            if valor is not None:
                linha.append(f"{valor:.2f}" if campo.lower() in ["temperatura", "umidade_ar", "umidade_solo", "luminosidade", "chuva", "uv"] else str(valor))
            else:
                linha.append("-")
        tabela_dados.append(linha)

    tabela = Table(tabela_dados)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004b9b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#AAAAAA")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#F5F5F5")]),
    ]))

    elementos.append(tabela)
    elementos.append(Spacer(1, 30))

    # --- 6. Rodapé institucional ---
    rodape_style = ParagraphStyle(
        name="Rodape",
        fontSize=9,
        alignment=1,
        textColor=colors.grey
    )
    data_emissao = datetime.now(tz).strftime("%d/%m/%Y %H:%M")
    elementos.append(Spacer(1, 20))
    elementos.append(HRFlowable(color=colors.HexColor("#CCCCCC"), thickness=0.7, width="100%"))
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(
        f"Relatório emitido em {data_emissao} pelo SIMC - Sistema Inteligente de Monitoramento Climático",
        rodape_style
    ))

    # --- 7. Gera PDF ---
    doc.build(elementos)
    return response
