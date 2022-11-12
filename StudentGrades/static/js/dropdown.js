let dropdown = document.querySelector('.dropdown-select');
let dropdownItem = document.querySelectorAll('.dropdown-select .menu li');

dropdown.addEventListener('click', (e) => {
  if (dropdown.classList.contains('closed')) {
    dropdown.classList.remove('closed');
    dropdown.classList.add('open');
  } else {
    dropdown.classList.add('closed');
    dropdown.classList.remove('open');
  }
});

for (let i = 0; i < dropdownItem.length; i++) {
  dropdownItem[i].addEventListener('click', function(event) {
    let dropdownItemClicked = document.querySelector('.menu li.active');
    if (dropdownItemClicked) dropdownItemClicked.classList.remove('active');
    event.target.classList.add('active');
  })
}

const options = document.querySelectorAll('.menu li')

const results = document.querySelectorAll('.tabbed-content div')
options.forEach(e => e.addEventListener('click', function() {
  results.forEach(f => f.style.display = f.id == e.dataset.target ? "block" : "none")
}))