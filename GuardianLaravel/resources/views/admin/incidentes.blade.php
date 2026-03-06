@extends('layouts.admin')

@section('content')

<style>

.page-title{
    font-weight:600;
    margin-bottom:20px;
}

.filter-card{
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

.table-container{
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
}

.table th{
    background:#f3f4f6;
    font-weight:600;
}

.badge-urgencia-alta{
    background:#ef4444;
    color:white;
    padding:5px 10px;
    border-radius:6px;
    font-size:12px;
}

.badge-urgencia-media{
    background:#f59e0b;
    color:white;
    padding:5px 10px;
    border-radius:6px;
    font-size:12px;
}

.badge-urgencia-baja{
    background:#10b981;
    color:white;
    padding:5px 10px;
    border-radius:6px;
    font-size:12px;
}

.badge-estado{
    background:#3b82f6;
    color:white;
    padding:5px 10px;
    border-radius:6px;
    font-size:12px;
}

.estado-select{
    border-radius:6px;
    padding:4px;
}

</style>


<h2 class="page-title">Gestión de Incidentes</h2>

<div class="filter-card">

<form class="row g-3">

    <div class="col-md-3">
        <label>Fecha</label>
        <input type="date" class="form-control">
    </div>

    <div class="col-md-3">
        <label>Urgencia</label>
        <select class="form-control">
            <option>Todas</option>
            <option>Alta</option>
            <option>Media</option>
            <option>Baja</option>
        </select>
    </div>

    <div class="col-md-3">
        <label>Estado</label>
        <select class="form-control">
            <option>Todos</option>
            <option>Pendiente</option>
            <option>En proceso</option>
            <option>Resuelto</option>
        </select>
    </div>

    <div class="col-md-3 d-flex align-items-end">
        <button class="btn btn-primary w-100">
            Filtrar
        </button>
    </div>

</form>

</div>


<div class="table-container">

<table class="table table-hover align-middle">

<thead>
<tr>
    <th>ID</th>
    <th>Zona</th>
    <th>Urgencia</th>
    <th>Estado</th>
    <th>Cambiar Estado</th>
</tr>
</thead>

<tbody>

<tr>
    <td>1</td>
    <td>Norte</td>

    <td>
        <span class="badge-urgencia-alta">
            Alta
        </span>
    </td>

    <td>
        <span class="badge-estado">
            Pendiente
        </span>
    </td>

    <td>
        <select class="form-control estado-select">
            <option>Pendiente</option>
            <option>En proceso</option>
            <option>Resuelto</option>
        </select>
    </td>

</tr>

<tr>
    <td>2</td>
    <td>Centro</td>

    <td>
        <span class="badge-urgencia-media">
            Media
        </span>
    </td>

    <td>
        <span class="badge-estado">
            En proceso
        </span>
    </td>

    <td>
        <select class="form-control estado-select">
            <option>Pendiente</option>
            <option selected>En proceso</option>
            <option>Resuelto</option>
        </select>
    </td>

</tr>

<tr>
    <td>3</td>
    <td>Sur</td>

    <td>
        <span class="badge-urgencia-baja">
            Baja
        </span>
    </td>

    <td>
        <span class="badge-estado">
            Resuelto
        </span>
    </td>

    <td>
        <select class="form-control estado-select">
            <option>Pendiente</option>
            <option>En proceso</option>
            <option selected>Resuelto</option>
        </select>
    </td>

</tr>

</tbody>

</table>

</div>

@endsection