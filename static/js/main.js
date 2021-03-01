
let course_dict = {}
const init = ()=>{
	
	const course_select = document.getElementsByClassName("course_select");
	const initial = course_select[0]
	for(let option of initial.options){
		if(initial.value !==option.value){
			course_dict[option.value] = option.innerHTML;
		}
	}

}
window.onload=init();


const createNewCourse = ()=>{
	const table = document.getElementById('table');
	const rows = table.rows;
	console.log(rows[0].childNodes[0]);
	let select = document.createElement('select');
	select.name=rows.length;
	select.setAttribute('class','custom-select custom-select-sm course_select');
	
	for(let key in course_dict){

		let option = document.createElement('option');
		option.value=key;
		option.text=course_dict[key];
		select.insertBefore(option,select.lastChild);
	}
	const td1 = document.createElement('td');
	// console.log(td1);
	
	const td2 = document.createElement('td');
	td2.text=rows.length+1;
	const tr = document.createElement('tr');
	// console.log(tr);
	tr.insertCell(td1);
	tr.insertCell(td2);
	table.appendChild(tr)
}





const add_btn = document.getElementById("add_btn");
add_btn.addEventListener('click',(e)=>{
	const course_select = document.getElementsByClassName("course_select");
	
	for(let select of course_select){
		if(course_dict[select.value]){
			delete course_dict[select.value];
		}
	}
	createNewCourse();

})


