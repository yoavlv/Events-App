import calendar
import csv
import io
from calendar import HTMLCalendar
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, redirect
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.pdfgen import canvas  # reportlab use to Generate PDF files

from .forms import VenueForm, EventForm
from .models import Event, Venue

from django.core.paginator import Paginator

# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "Yoav"
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create a Calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get the time now
    time = now.strftime("%I:%M:%S %p")

    return render(request, 'home.html', {"name":name , "month":month,"year":year ,"month_number":month_number,"cal":cal, "current_year": current_year,"time":time})



# # Generate a PDF file venue list
# def venue_pdf(request):
#     # Create Bytestream buffer
#     buf = io.BytesIO()
#     # Create a Canvas
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0 )
#     # Create a text object - what to put on the canvas
#     textob = c.beginText()
#     textob.setTextOrigin(inch,inch)
#     textob.setFont("Helvetica", 14 )
#
#     # Designate The Model
#     venues = Venue.objects.all()
#     lines = []
#
#     for venue in venues:
#         lines.append(venue.name)
#         lines.append(venue.address)
#         lines.append(venue.zip_code)
#         lines.append(venue.phone)
#         lines.append(venue.web)
#         lines.append(venue.email_address)
#         lines.append("===================") # Blank Line
#
#     for line in lines:
#         textob.textLine(line)
#
#     # Finish up
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)
#
#     return FileResponse(buf, as_attachment=True, filename="venue.pdf")




# Generate csv file venue list
def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Dispositions'] = 'attachment; filename=venues.csv'

    # Create a csv writer - put the staff in csv file
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    # Add column heading to the CSV file

    writer.writerow(["Venue Name", "Address", "Zip Code", "Phone", "Web", "Email Address"])

    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])
    return response


# Generate text file venue list
def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response['Content-Dispositions'] = 'attachment; filename=venues.txt'
    # Designate The Model
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n')

    response.writelines(lines)
    return response





def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)  # Get a specific item from DB
    form = EventForm(request.POST or None , instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, "update_event.html", {'event': event, "form":form})



def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_event?submitted=True")
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_event.html', {'form':form, "submitted":submitted})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)  # Get a specific item from DB
    event.delete()
    return redirect("list-events")


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # Get a specific item from DB
    venue.delete()
    return redirect("list-venues")


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # Get a specific item from DB
    form = VenueForm(request.POST or None , instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, "update_venue.html", {'venue': venue, "form":form})



def search_venue(request):
    if request.method == "POST":
        searched = request.POST["searched"] # Grab the search item
        venues = Venue.objects.filter(name__contains =searched)
        return render(request, "search_venues.html", {'searched': searched, 'venues': venues})
    else:
        return render(request, "search_venues.html")




def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # Get a specific item from DB
    return render(request, 'show_venue.html', {'venue': venue})



def list_venues(request):
    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(),1)  # How many arg show for page we want to show
    page = request.GET.get("page")
    venues = p.get_page(page)

    return render(request, 'venue.html', {"venue_list":venue_list,"venues":venues})




def all_events(request):
    #Grab everything from the DB
    event_list = Event.objects.all().order_by('?') # $ = random - DB intensive
    return render(request, 'event_list.html', {"event_list": event_list})




def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_venue.html', {'form':form, "submitted":submitted})

