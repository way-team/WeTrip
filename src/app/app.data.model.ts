
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

