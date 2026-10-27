"""Render SVG to vector PDF using installed librsvg and Cairo, including clips."""
import ctypes as c
from ctypes.util import find_library
from pathlib import Path

class Rectangle(c.Structure):
    _fields_=[('x',c.c_double),('y',c.c_double),('width',c.c_double),('height',c.c_double)]

class Error(c.Structure):
    _fields_=[('domain',c.c_uint),('code',c.c_int),('message',c.c_char_p)]

RSVG=c.CDLL(find_library('rsvg-2'))
CAIRO=c.CDLL(find_library('cairo'))
OBJECT=c.CDLL(find_library('gobject-2.0'))
GLIB=c.CDLL(find_library('glib-2.0'))
RSVG.rsvg_handle_new_from_data.argtypes=[c.c_char_p,c.c_size_t,c.POINTER(c.POINTER(Error))]
RSVG.rsvg_handle_new_from_data.restype=c.c_void_p
RSVG.rsvg_handle_render_document.argtypes=[c.c_void_p,c.c_void_p,c.POINTER(Rectangle),c.POINTER(c.POINTER(Error))]
RSVG.rsvg_handle_render_document.restype=c.c_int
CAIRO.cairo_pdf_surface_create.argtypes=[c.c_char_p,c.c_double,c.c_double]
CAIRO.cairo_pdf_surface_create.restype=c.c_void_p
CAIRO.cairo_create.argtypes=[c.c_void_p]
CAIRO.cairo_create.restype=c.c_void_p
for name in ('cairo_destroy','cairo_surface_finish','cairo_surface_destroy'):
    getattr(CAIRO,name).argtypes=[c.c_void_p]
CAIRO.cairo_status.argtypes=[c.c_void_p]
CAIRO.cairo_surface_status.argtypes=[c.c_void_p]
OBJECT.g_object_unref.argtypes=[c.c_void_p]
GLIB.g_error_free.argtypes=[c.POINTER(Error)]

def svg_to_pdf(svg,path,width=600,height=750):
    error=c.POINTER(Error)()
    data=svg.encode()
    handle=RSVG.rsvg_handle_new_from_data(data,len(data),c.byref(error))
    if not handle:
        message=error.contents.message.decode() if error else 'SVG parse failed'
        if error:GLIB.g_error_free(error)
        raise ValueError(message)
    surface=CAIRO.cairo_pdf_surface_create(str(Path(path)).encode(),width,height)
    context=CAIRO.cairo_create(surface)
    try:
        viewport=Rectangle(0,0,width,height)
        if not RSVG.rsvg_handle_render_document(handle,context,c.byref(viewport),c.byref(error)):
            message=error.contents.message.decode() if error else 'SVG render failed'
            if error:GLIB.g_error_free(error)
            raise ValueError(message)
        if CAIRO.cairo_status(context):raise RuntimeError('Cairo drawing failed')
        CAIRO.cairo_surface_finish(surface)
        if CAIRO.cairo_surface_status(surface):raise RuntimeError('PDF surface failed')
    finally:
        CAIRO.cairo_destroy(context)
        CAIRO.cairo_surface_destroy(surface)
        OBJECT.g_object_unref(handle)
