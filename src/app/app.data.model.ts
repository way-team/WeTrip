
export class User {
  username: string;
  email: string;
  password: string;
  name: string;
  lastName: string;
  birthdate: Date;
  gender: string;
  nationality: string;
  city: string;
  photo: string;
  status: boolean;
  mediumRate: number;
  numRate: number;
  isPremium: boolean;
  isSuperUser: boolean;
  description: string;
}

export class Trip {
  title: String;
  description: String;
  startDate: Date;
  endDate: Date;
  type: String;
  image: String;
  status: Boolean;
  country: String;
  city: String;

}

export class test {
  count: string;
  next: string;
  previous: string;
  results: User[];
}
