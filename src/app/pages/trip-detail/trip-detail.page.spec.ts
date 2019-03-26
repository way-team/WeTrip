import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Trip-detailPage } from './trip-detail.page';

describe('HomePage', () => {
  let component: TripDetailPage;
  let fixture: ComponentFixture<Trip-detailPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Trip-detailPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Trip-detailPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
