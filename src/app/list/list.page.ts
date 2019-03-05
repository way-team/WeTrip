import { Component, OnInit } from '@angular/core';
import { test } from '../app.data.model';
import { DataManagement } from '../services/dataManagement';

@Component({
	selector: 'app-list',
	templateUrl: 'list.page.html',
	styleUrls: ['list.page.scss']
})
export class ListPage implements OnInit {
	private selectedItem: any;
	private icons = [
		'flask',
		'wifi',
		'beer',
		'football',
		'basketball',
		'paper-plane',
		'american-football',
		'boat',
		'bluetooth',
		'build',
	];
	public items: Array<{ title: string; note: string; icon: string }> = [];
	constructor(
		public dataManagement: DataManagement
	) {
		for (let i = 1; i < 11; i++) {
			this.items.push({
				title: 'Item ' + i,
				note: 'This is item #' + i,
				icon: this.icons[Math.floor(Math.random() * this.icons.length)]
			});
		}
	}

	public response: test;

	public getText(): void {
		console.log("Button pressed");
		this.dataManagement.test().then(data => {
			this.response = data;
		})
	}

	ngOnInit() {
	}
	// add back when alpha.4 is out
	// navigate(item) {
	//   this.router.navigate(['/list', JSON.stringify(item)]);
	// }
}
