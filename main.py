# -------------------------------------------------------------------------
# Project: MTI IEEE Smart Library Management System
# Developer: Sondos (Faculty of CS & AI)
# Architecture: Data-Centric CRUD Operations
# Version: 1.0 (Stable Release)
# ---------------------------------------------------------
# Note: This project implements automated logic to simulate 
# intelligent book reservation, laying the foundation for 
# future AI-driven recommendation features.
# -------------------------------------------------------------------------

import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize professional terminal interface
console = Console()
DATA_FILE = "library_data.json"
library_books = []

def load_data():
    """
    Synchronizes local memory with the JSON database.
    Includes a 'Self-Healing' mechanism to validate and fix missing data keys.
    """
    global library_books
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                raw_data = json.load(file)
                # Validation Loop: Ensures data integrity for each book object
                for book in raw_data:
                    if "status" not in book: book["status"] = "Available"
                    if "borrower" not in book: book["borrower"] = "N/A"
                    if "date" not in book: book["date"] = "N/A"
                    if "shelf" not in book: book["shelf"] = "General"
                    if "category" not in book: book["category"] = "Academic"
                library_books = raw_data
        except Exception:
            library_books = []

def save_data():
    """
    Updates the physical JSON file with current session modifications.
    Uses Indentation for human-readable formatting (Prettified JSON).
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(library_books, file, indent=4)
    except Exception as e:
        console.print(f"[bold red]❌ Database Sync Error: {e}[/bold red]")

# Trigger initial data synchronization
load_data()

while True:
    # Main Application Dashboard
    console.print("\n", Panel.fit("   MTI UNIVERSITY - SMART LIBRARY SYSTEM   ", style="bold white on blue"))
    console.print("[1] [bold cyan]Display Catalog (Metadata & Inventory)[/bold cyan]")
    console.print("[2] [bold green]Initiate Reservation (Process Borrower Data)[/bold green]")
    console.print("[3] [bold yellow]Revert Reservation (Cancellation Logic)[/bold yellow]")
    console.print("[4] [bold red]Terminate Session[/bold red]")
    
    choice = input("\nSelect Action (1-4): ")
    
    if choice == "1":
        # Logic for rendering the inventory table
        if not library_books:
            console.print("[bold red]❌ Error: No records found in library_data.json.[/bold red]")
            continue
            
        table = Table(title="MTI University Library Inventory")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Book Title", style="white")
        table.add_column("Category", style="blue")
        table.add_column("Status", justify="center")
        table.add_column("Reserved By", style="magenta")
        table.add_column("Return Deadline", style="yellow")
        
        for i, b in enumerate(library_books, 1):
            st = b.get('status', 'Available')
            color = "green" if st == "Available" else "red"
            
            table.add_row(
                str(i), 
                b.get('title', 'Unknown'), 
                b.get('category', 'General'),
                f"[{color}]{st}[/{color}]",
                b.get('borrower', 'N/A'),
                b.get('date', 'N/A')
            )
        console.print(table)

    elif choice == "2":
        # Logic for book reservation and deadline calculation
        try:
            book_id = int(input("Enter Book ID to reserve: ")) - 1
            if 0 <= book_id < len(library_books):
                selected = library_books[book_id]
                
                if selected.get('status') == "Available":
                    user_name = input("Enter Borrower's Full Name: ").strip()
                    if not user_name:
                        console.print("[bold red]❌ Input Error: Borrower name is mandatory.[/bold red]")
                        continue
                        
                    # Calculate return deadline (Current Time + 14 Days)
                    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                    
                    # Update object state in memory
                    selected['status'] = "Reserved"
                    selected['borrower'] = user_name
                    selected['date'] = due_date
                    
                    # Persist changes to the database
                    save_data()
                    console.print(Panel(
                        f"✅ [bold green]Reservation Successful![/bold green]\n\n"
                        f"Book: {selected['title']}\n"
                        f"Assigned To: [cyan]{user_name}[/cyan]\n"
                        f"Return Deadline: [bold yellow]{due_date}[/bold yellow]",
                        title="Transaction Receipt"
                    ))
                else:
                    console.print(f"[bold red]❌ Status Error: Already reserved by {selected.get('borrower')}[/bold red]")
            else:
                console.print("[bold red]❌ Index Error: ID not found in catalog.[/bold red]")
        except ValueError:
            console.print("[bold red]❌ Type Error: ID must be a numeric integer.[/bold red]")

    elif choice == "3":
        # Logic for resetting book status
        try:
            book_id = int(input("Enter Book ID to cancel: ")) - 1
            if 0 <= book_id < len(library_books):
                selected = library_books[book_id]
                if selected.get('status') == "Reserved":
                    selected['status'] = "Available"
                    selected['borrower'] = "N/A"
                    selected['date'] = "N/A"
                    save_data()
                    console.print("[bold green]✅ Success: Reservation cancelled and database updated.[/bold green]")
                else:
                    console.print("[bold red]❌ Logical Error: Selected book is not reserved.[/bold red]")
        except:
            console.print("[bold red]❌ Error: Unable to process cancellation.[/bold red]")

    elif choice == "4":
        # Graceful application shutdown
        console.print("[bold magenta]Closing Secure Database... Goodbye Sondos! 👋[/bold magenta]")
        break
