#!/usr/bin/env python
"""
Script de diagnóstico para Google OAuth.
Verifica configuración de Site, credenciales y configuración de allauth.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.sites.models import Site
from django.conf import settings
from allauth.socialaccount.models import SocialApp

print("=" * 60)
print("🔍 DIAGNÓSTICO DE GOOGLE OAUTH")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1️⃣  VARIABLES DE ENTORNO")
print("-" * 60)
client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

if client_id:
    print(f"✅ GOOGLE_OAUTH_CLIENT_ID: {client_id[:30]}...")
else:
    print("❌ GOOGLE_OAUTH_CLIENT_ID: NO ENCONTRADO")

if client_secret:
    print(f"✅ GOOGLE_OAUTH_CLIENT_SECRET: {client_secret[:15]}...")
else:
    print("❌ GOOGLE_OAUTH_CLIENT_SECRET: NO ENCONTRADO")

# 2. Verificar SITE_ID en settings
print("\n2️⃣  CONFIGURACIÓN DE SITE")
print("-" * 60)
print(f"SITE_ID en settings.py: {settings.SITE_ID}")

# 3. Verificar Sites en la base de datos
print("\n3️⃣  SITES EN LA BASE DE DATOS")
print("-" * 60)
try:
    sites = Site.objects.all()
    if sites.exists():
        for site in sites:
            print(
                f"{'✅' if site.id == settings.SITE_ID else '⚠️ '} Site ID {site.id}: {site.domain} ({site.name})"
            )
    else:
        print("❌ NO HAY SITES EN LA BASE DE DATOS")
        print("\nSOLUCIÓN: Ejecuta el siguiente comando:")
        print("python manage.py shell")
        print(">>> from django.contrib.sites.models import Site")
        print(">>> Site.objects.create(id=1, domain='localhost:8000', name='MiXiaomi')")
except Exception as e:
    print(f"❌ Error al consultar Sites: {e}")

# 4. Verificar Site con SITE_ID configurado
print("\n4️⃣  SITE CONFIGURADO (SITE_ID=1)")
print("-" * 60)
try:
    site = Site.objects.get(id=settings.SITE_ID)
    print(f"✅ Site encontrado:")
    print(f"   ID: {site.id}")
    print(f"   Domain: {site.domain}")
    print(f"   Name: {site.name}")
except Site.DoesNotExist:
    print(f"❌ NO EXISTE SITE CON ID={settings.SITE_ID}")
    print("\nSOLUCIÓN: Ejecuta:")
    print(f"python manage.py shell")
    print(f">>> from django.contrib.sites.models import Site")
    print(
        f">>> Site.objects.create(id={settings.SITE_ID}, domain='localhost:8000', name='MiXiaomi')"
    )

# 5. Verificar SocialApp (si se usa configuración via admin)
print("\n5️⃣  SOCIAL APPS (Configuración vía Admin)")
print("-" * 60)
try:
    social_apps = SocialApp.objects.filter(provider="google")
    if social_apps.exists():
        for app in social_apps:
            print(f"⚠️  SocialApp encontrada: {app.name}")
            print(
                f"   Client ID: {app.client_id[:30]}..."
                if app.client_id
                else "   ❌ Sin Client ID"
            )
            print(f"   Secret: {'Configurado' if app.secret else '❌ Sin Secret'}")
            print(f"   Sites: {[s.domain for s in app.sites.all()]}")
            print(
                "\n⚠️  IMPORTANTE: Estás usando VARIABLES DE ENTORNO para las credenciales."
            )
            print("   Las SocialApp en el admin NO SE USAN cuando configuras via .env")
    else:
        print(
            "✅ No hay SocialApps configuradas (correcto si usas variables de entorno)"
        )
except Exception as e:
    print(f"❌ Error al consultar SocialApps: {e}")

# 6. Verificar configuración de SOCIALACCOUNT_PROVIDERS
print("\n6️⃣  CONFIGURACIÓN EN settings.py")
print("-" * 60)
providers = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
google_config = providers.get("google", {})
app_config = google_config.get("APP", {})

print(f"SOCIALACCOUNT_PROVIDERS configurado: {'✅' if providers else '❌'}")
print(f"Configuración de Google: {'✅' if google_config else '❌'}")

if app_config:
    config_client_id = app_config.get("client_id")
    config_secret = app_config.get("secret")

    print(f"\nAPP config en settings:")
    if config_client_id:
        print(f"  ✅ client_id: {config_client_id[:30]}...")
    else:
        print(f"  ❌ client_id: NO CONFIGURADO")

    if config_secret:
        print(f"  ✅ secret: {config_secret[:15]}...")
    else:
        print(f"  ❌ secret: NO CONFIGURADO")
else:
    print("⚠️  APP config no encontrado en settings.py")

# 7. URLs configuradas
print("\n7️⃣  URLS DE ALLAUTH")
print("-" * 60)
print("✅ Asegúrate de tener en urls.py:")
print('   path("accounts/", include("allauth.urls"))')
print("\nCallback URL esperado:")
print("   http://localhost:8000/accounts/google/login/callback/")
print("\n⚠️  Este DEBE estar configurado en Google Cloud Console")

# Resumen
print("\n" + "=" * 60)
print("📋 RESUMEN")
print("=" * 60)

issues = []
if not client_id or not client_secret:
    issues.append("❌ Faltan variables de entorno en .env")
if not Site.objects.filter(id=settings.SITE_ID).exists():
    issues.append(f"❌ No existe Site con ID={settings.SITE_ID}")

if issues:
    print("\n🚨 PROBLEMAS ENCONTRADOS:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n✅ Configuración parece correcta")
    print("\nSi sigue fallando, verifica en Google Cloud Console:")
    print("   1. URIs de redireccionamiento autorizados:")
    print("      http://localhost:8000/accounts/google/login/callback/")
    print("   2. Orígenes autorizados:")
    print("      http://localhost:8000")

print("\n" + "=" * 60)
