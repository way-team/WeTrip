import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TripsResultsPage } from './trips-results.page';

describe('TripsResultsPage', () => {
  let component: TripsResultsPage;
  let fixture: ComponentFixture<TripsResultsPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TripsResultsPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TripsResultsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
