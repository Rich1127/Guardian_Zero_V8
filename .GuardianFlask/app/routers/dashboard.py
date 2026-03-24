from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import (
    db, Reporte, Alertas, Voluntario,
    Recursos, ZonaAfectada, AsignacionRecursos
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():

    # ── Incidentes ──────────────────────────────────────────
    total_reportes     = Reporte.query.count()
    reportes_criticos  = Reporte.query.filter_by(Prioridad="Critica").count()
    reportes_alta      = Reporte.query.filter_by(Prioridad="Alta").count()
    reportes_activos   = Reporte.query.filter(
        Reporte.Estatus.in_(["Pendiente", "En Proceso"])
    ).count()
    reportes_finalizados = Reporte.query.filter_by(Estatus="Finalizado").count()

    # ── Tipos de desastre (conteo por Tipo_Zona en zona_afectada) ───────────
    tipos_raw = (
        db.session.query(ZonaAfectada.Tipo_Zona, func.count(ZonaAfectada.ID))
        .group_by(ZonaAfectada.Tipo_Zona)
        .all()
    )
    # Mapeamos a un dict para el template
    tipos_desastre = {t: c for t, c in tipos_raw if t}
    total_tipos    = sum(tipos_desastre.values()) or 1  # evitar div/0

    # ── Voluntarios ──────────────────────────────────────────
    total_voluntarios   = Voluntario.query.filter_by(Estatus="Activo").count()
    vol_en_mision       = Voluntario.query.filter_by(Estatus="En Mision").count()

    # ── Zonas afectadas ──────────────────────────────────────
    zonas_criticas      = ZonaAfectada.query.filter(
        ZonaAfectada.Nivel_Gravedad.in_(["Critico", "Desastre Total"])
    ).count()
    zonas_moderadas     = ZonaAfectada.query.filter_by(Nivel_Gravedad="Moderado").count()
    zonas_estables      = ZonaAfectada.query.filter_by(Nivel_Gravedad="Estable").count()
    total_zonas         = ZonaAfectada.query.count() or 1

    # Población total afectada
    pop_result = db.session.query(
        func.sum(ZonaAfectada.Poblacion_Afectada)
    ).scalar()
    poblacion_afectada  = pop_result or 0

    # ── Recursos ─────────────────────────────────────────────
    recursos_asignados  = db.session.query(
        func.sum(AsignacionRecursos.Cantidad_Asignada)
    ).scalar() or 0

    # ── Alertas recientes ─────────────────────────────────────
    alertas_recientes = (
        Alertas.query
        .order_by(Alertas.Fecha_Emision.desc())
        .limit(5)
        .all()
    )
    alertas_evacuacion = Alertas.query.filter_by(Nivel_Alerta="Evacuacion").count()
    alertas_precaucion = Alertas.query.filter_by(Nivel_Alerta="Precaucion").count()

    # ── Zonas para el mapa (con coordenadas cargadas) ────────
    # Coordenadas deben estar en formato "lat,lng" en la BD
    zonas_mapa = (
        ZonaAfectada.query
        .filter(ZonaAfectada.Coordenadas.isnot(None))
        .all()
    )
    # Serializar para pasar a JS como JSON
    zonas_json = []
    for z in zonas_mapa:
        try:
            partes = z.Coordenadas.strip().split(",")
            lat = float(partes[0])
            lng = float(partes[1])
            zonas_json.append({
                "lat":      lat,
                "lng":      lng,
                "nombre":   z.Nombre_Zona or "Sin nombre",
                "tipo":     z.Tipo_Zona or "General",
                "gravedad": z.Nivel_Gravedad or "Estable",
                "poblacion": z.Poblacion_Afectada or 0,
            })
        except Exception:
            pass  # Coordenada mal formateada, se omite

    # ── Nivel de preparación por estado (reportes por zona) ──
    estados_prep = (
        db.session.query(
            ZonaAfectada.Nombre_Zona,
            ZonaAfectada.Nivel_Gravedad,
            func.count(Reporte.ID).label("total_rep")
        )
        .outerjoin(Reporte, Reporte.ID_Zona_Afectada == ZonaAfectada.ID)
        .group_by(ZonaAfectada.ID)
        .order_by(func.count(Reporte.ID).desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        # Incidentes
        total_reportes       = total_reportes,
        reportes_criticos    = reportes_criticos,
        reportes_alta        = reportes_alta,
        reportes_activos     = reportes_activos,
        reportes_finalizados = reportes_finalizados,
        # Desastres
        tipos_desastre       = tipos_desastre,
        total_tipos          = total_tipos,
        # Voluntarios
        total_voluntarios    = total_voluntarios,
        vol_en_mision        = vol_en_mision,
        # Zonas
        zonas_criticas       = zonas_criticas,
        zonas_moderadas      = zonas_moderadas,
        zonas_estables       = zonas_estables,
        total_zonas          = total_zonas,
        poblacion_afectada   = poblacion_afectada,
        # Recursos
        recursos_asignados   = recursos_asignados,
        # Alertas
        alertas_recientes    = alertas_recientes,
        alertas_evacuacion   = alertas_evacuacion,
        alertas_precaucion   = alertas_precaucion,
        # Mapa
        zonas_json           = zonas_json,
    )