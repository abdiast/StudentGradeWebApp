function addRow() {
    // get input values
    var Coursename = document.getElementById('currentAge').value;
    var TeachName = document.getElementById('name').value;
    var Birthday = document.getElementById('Birthday').value;
    var carType = "0/10";//document.getElementById('carType').value;
  
    var table = document.getElementsByTagName('table')[0];
    const index = table.rows.length;
    console.log(table)
    var newRow = table.insertRow(index);
    if(index % 2 === 0)
    {
        newRow.classList.add("active-row")
    }
    else
    {
        newRow.classList.remove("active-row")
    }
    
    newRow.setAttribute('data-index', index);
    var cel1 = newRow.insertCell(0);
    var cel2 = newRow.insertCell(1);
    var cel3 = newRow.insertCell(2);
    var cel4 = newRow.insertCell(3);
    var cel5 = newRow.insertCell(4);
  
    cel1.textContent = Coursename;
    cel2.textContent = TeachName;
    cel3.textContent = Birthday;
    cel4.textContent = carType;
    cel5.innerHTML = '<button onclick="removeRow(this)" type="button" class="delete-button">Delete</button>';
  }
  
  
  function myFunction() {
    var x = document.getElementById("table").rows.length;
    document.getElementById("demo").innerHTML = "Found " + x + "tr elements in the table.";
  }
  
  
  function removeRow(evt) {
    const deleteIndex = evt.parentElement.parentElement.rowIndex;
    console.log(deleteIndex)
    document.getElementById("table").deleteRow(deleteIndex);
  }

