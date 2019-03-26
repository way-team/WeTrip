
export class UserProfile {
  user: User;
  email: string;
  first_name: string;
  last_name: string;
  description: string;
  birthdate: string;
  city: string;
  nationality: string;
  photo: string;
  discoverPhoto: string;
  averageRate: Number;
  numRate: Number;
  isPremium: boolean;
  status: boolean;
  gender: string;
  language: string;
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


export class User {
  id: Number;
  username: string;
}

export class test {
  count: string;
  next: string;
  previous: string;
  results: User[];
}

