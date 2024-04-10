from copy import copy, deepcopy

from django.db.models.query import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.query import QuerySet

from clubs.models import Club
from users.models import RoleUser


class TestView(TestCase):
    """
    Template for testing views
    """
    class Meta:
        abstract = True

    @classmethod
    def setUpTestData(cls) -> None:

        # Create test user data
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )

        # Create model data
        if cls.createModelData:
            cls.createModelData(cls)

        return super().setUpTestData()
    

    ########################
    # Full assertion funcs #
    ########################


    def assertPageView(
        self,
        url,
        url_args,
        template,
        context,
        anon_user_access,
        denied_access_roles,
        allowed_access_roles,
        club_denied,
        club_allowed
    ):
        """
        Tests all functions of a page view at the same time.
        Structure to copy:

        self.assertPageView(
            url="",
            url_args={
            },
            template="",
            context={
            },
            anon_user_access=False,
            denied_access_roles=[],
            allowed_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )

        """
        self.loop_first(
            funcs=[
                self.loop_users,
                self.loop_club,
                self.loop_parameters,
                self.loop_final_template,
            ],
            data={
                "url": url,
                "url_args": url_args,
                "template": template,
                "context": context,
                "anon_user_access": anon_user_access,
                "denied_access_roles": denied_access_roles,
                "allowed_access_roles": allowed_access_roles,
                "club_denied": club_denied,
                "club_allowed": club_allowed,
            },
            used_data={},
            full_url=reverse(url, kwargs=url_args)
        )
        
    
    def assertPostView(
        self,
        url,
        url_args,
        redirect_url,
        post_data,
        anon_user_access,
        denied_access_roles,
        allowed_access_roles,
        club_denied,
        club_allowed
    ):
        """
        Tests all functions of a POST view at the same time.
        Structure to copy:

        self.assertPostView(
            url="",
            url_args={
            }
            redirect_url=reverse(""),
            post_date={
            }
            anon_user_access=False,
            denied_access_roles=[],
            allowed_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )

        """
        self.loop_first(
            funcs=[
                self.loop_users,
                self.loop_club,
                self.loop_post_data,
                self.loop_parameters,
                self.loop_final_post,
            ],
            data={
                "url": url,
                "url_args": url_args,
                "redirect_url": redirect_url,
                "post_data": post_data,
                "anon_user_access": anon_user_access,
                "denied_access_roles": denied_access_roles,
                "allowed_access_roles": allowed_access_roles,
                "club_denied": club_denied,
                "club_allowed": club_allowed,
            },
            used_data={},
            full_url=reverse(url, kwargs=url_args)
        )


    #####################
    # Req looping funcs #
    #####################
        
    
    def get_next_func(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Calls the next function and checks for errors
        """
        # Copy the list to create multiple threads of testing
        funcs_copy = copy(funcs)

        try:
            next_func = funcs_copy.pop(0)
        except IndexError:
            raise ValueError("List of functions did not end with a loop_final.")
        
        next_func(funcs_copy, data, used_data, full_url)
    
    
    def loop_first(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Call to start the loop
        """
        self.get_next_func(funcs, data, used_data, full_url)

                
    def loop_users(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Creates a new test case for each user type
        """        
        anon_user_access = data.get("anon_user_access")
        denied_access_roles = data.get("denied_access_roles")
        allowed_access_roles = data.get("allowed_access_roles")
        post_data = data.get("post_data")

        # Data type verification
        if type(anon_user_access) is not bool:
            raise ValueError("Type of anon_user_access must be bool.")
        if type(denied_access_roles) is not list:
            raise ValueError("Type of denied_access_roles must be list of roles.")
        if type(allowed_access_roles) is not list:
            raise ValueError("Type of allowed_access_roles must be list of roles.")
        if any(type(role) is not RoleUser.Roles for role in denied_access_roles):
            raise ValueError("Type of denied_access role must be role.")
        if any(type(role) is not RoleUser.Roles for role in allowed_access_roles):
            raise ValueError("Type of allowed_access role must be role.")
        
        # Check anon access
        self.client.logout()
        
        used_data["role"] = "Anonymous user"
        if anon_user_access:
            self.get_next_func(funcs, data, used_data, full_url)
        else:
            try:
                self.assertHttpResponseForbidden(full_url, post_data)
            except AssertionError as e:
                raise AssertionError(f"Improper response code for '{full_url}'. Data: {used_data}. Error: {e}")

        # Check for access denied
        for role in denied_access_roles:
            used_data["role"] = role

            self.client.force_login(self.user)
            self.user.role = role
            self.user.save()

            try:
                self.assertHttpResponseForbidden(full_url, post_data)
            except AssertionError as e:
                raise AssertionError(f"Improper response code for '{full_url}'. Data: {used_data}. Error: {e}")

        # Check for access allowed
        for role in allowed_access_roles:
            used_data["role"] = role

            self.client.force_login(self.user)
            self.user.role = role
            self.user.save()

            self.get_next_func(funcs, data, used_data, full_url)


    def loop_club(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Creates a new test case for when a club is required
        """        
        club_denied = data.get("club_denied")
        club_allowed = data.get("club_allowed")
        post_data = data.get("post_data")

        # Check that club_denied and club_required is False or club instance
        if club_denied is not None and not isinstance(club_denied, Club):
            raise ValueError("Type of club_denied must be either None or instance of Club.")
        if club_allowed is not None and not isinstance(club_allowed, Club):
            raise ValueError("Type of club_allowed must be either None or instance of Club.")
        
        # Check for denied club (only for non-admin)
        if club_denied is not None and self.user.role is not RoleUser.Roles.ADMIN:
            used_data["club"] = club_denied

            self.user.club = club_denied
            self.user.save()

            try:
                self.assertHttpResponseForbidden(full_url, post_data)
            except AssertionError as e:
                raise AssertionError(f"Improper response code for '{full_url}'. Data: {used_data}. Error: {e}")

        # Check for allowed club
        if club_allowed is not None:
            used_data["club"] = club_allowed
            
            self.user.club = club_allowed
            self.user.save()

            self.get_next_func(funcs, data, used_data, full_url)

        # Check other cases
        if club_denied is None and club_allowed is None:
            self.get_next_func(funcs, data, used_data, full_url)

    
    def loop_parameters(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Creates a new test case for each parameter
        """        
        url = data.get("url")
        url_args = data.get("url_args")
        post_data = data.get("post_data")

        for arg, v in url_args.items():
            # Replace current arg with a different value
            temp_args = deepcopy(url_args)
            temp_args[arg] = 0 if type(v) is int else None

            used_data["parameters"] = temp_args

            try:
                self.assertHttpResponseNotFound(reverse(url, kwargs=temp_args), post_data)
            except AssertionError:
                raise AssertionError(f"Parameter error. Parameters '{temp_args}' were able to access '{full_url}'. Data: {used_data}")

        used_data["parameters"] = url_args
        self.get_next_func(funcs, data, used_data, full_url)


    def loop_post_data(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Creates a new test case for each post data
        """        
        url = data.get("url")
        post_data = data.get("post_data")

        # Check post data raises errors
        for k in post_data.keys():

            # Replace current arg with a different value
            temp_data = deepcopy(post_data)
            temp_data[k] = ""

            used_data["post_data"] = temp_data

            try:
                self.assertHttpResponseBadRequest(full_url, temp_data)
            except AssertionError:
                raise AssertionError(f"Post data error. Able to access '{full_url}' with post data {temp_data}. Data: {used_data}")

        used_data["post_data"] = post_data
        self.get_next_func(funcs, data, used_data, full_url)


    def loop_final_template(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Final func in the loop, checks that func works as intended (for template)
        """

        # Check if funcs are left
        if len(funcs) > 1:
            raise ValueError("funcs has too many arguments left. loop_final must be final item.")

        template = data.get("template")
        context = data.get("context")

        try:
            self.assertTemplateView(full_url, template, context)
        except AssertionError as e:
            raise AssertionError(f"'{full_url}' did not return the proper information. Data: {used_data}. Error: {e}")


    def loop_final_post(self, funcs: list, data: dict, used_data: dict, full_url: str):
        """
        Final func in the loop, checks that func works as intended (for post data)
        """

        # Check if funcs are left
        if len(funcs) > 1:
            raise ValueError("funcs has too many arguments left. loop_final must be final item.")

        redirect_url = data.get("redirect_url")
        post_data = data.get("post_data")

        try:
            self.assertPostRedirectsToPage(full_url, redirect_url, post_data)
        except AssertionError as e:
            raise AssertionError(f"'{full_url}' did not properly redirect. Data: {used_data}. Error: {e}")
        

    ##############
    # Assertions #
    ##############


    def assertHttpResponseNotFound(self, url, data):
        """
        Asserts that the provided url returns an HttpResponseNotFound statuscode
        """
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
        response = self.client.post(url, follow=True, data=data)
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
    

    def assertHttpResponseForbidden(self, url, data):
        """
        Asserts that the provided url returns an HttpResponseForbidden statuscode
        """

        response = self.client.get(url, follow=True)
        try:
            self.assertEqual(response.status_code, HttpResponseForbidden.status_code)
        except AssertionError as e:
            raise AssertionError(f"Get request did not return HttpResponseForbidden. Returned {response} instead.")
        response = self.client.post(url, follow=True, data=data)
        try:
            self.assertEqual(response.status_code, HttpResponseForbidden.status_code)
        except AssertionError as e:
            raise AssertionError(f"Post request did not return HttpResponseForbidden. Returned {response} instead.")


    def assertHttpResponseBadRequest(self, url, data):
        """
        Asserts that the provided url returns an HttpResponseBadRequest statuscode (exclusively for POST)
        """
        # Catch model access errors
        try:
            response = self.client.post(url, follow=True, data=data)
            self.assertEqual(response.status_code, HttpResponseBadRequest.status_code)
        except ValueError as e:
            raise AssertionError(f"Model exception error occured at url {url}. Error: {e}")

    
    def assertTemplateView(self, url, template, context={}):
        """
        Asserts that the provided url returns the proper page, template, and context
        """
        try:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
            for k, v in context.items():
                # Convert querysets to lists
                if isinstance(v, QuerySet):
                    self.assertEqual(list(response.context.get(k)), list(v))
                else:
                    self.assertEqual(response.context.get(k), v)

            response = self.client.post(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
            for k, v in context.items():
                # Convert querysets to lists
                if isinstance(v, QuerySet):
                    self.assertEqual(list(response.context.get(k)), list(v))
                else:
                    self.assertEqual(response.context.get(k), v)
                    
        except AssertionError as e:
            raise AssertionError(f"Response: {response}. Error: {e}")


    def assertPostRedirectsToPage(self, url, redirect_url, data):
        """
        Asserts that the provided url redirects to another page succesfully (exclusively for post)
        """
        response = self.client.post(url, follow=True, data=data)
        if (response.status_code != 200):
            raise AssertionError(f"Function returning error code {response.status_code}. {response.content}")
        try:
            self.assertRedirects(response, redirect_url)
        except AssertionError as e:
            if response.__getitem__("Content-Type") == "text":
                raise AssertionError(response.content)
            else:
                raise AssertionError(e)
    


class TestModel(TestCase):
    """
    Template for testing models
    """
    class Meta:
        abstract = True

    @classmethod
    def setUpTestData(cls) -> None:

        # Create test user data
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )

        # Create model data
        if cls.createModelData:
            cls.createModelData(cls)

        return super().setUpTestData()
    

    def assertModelCreation(self, data):
        """
        Checks that the model is created correctly
        
        Syntax:
        {
            model1: {
                field1: "val1",
                field2: "val2",
            }
        }
        """
        for model, fields in data.items():
            for k, v in fields.items():
                self.assertEqual(getattr(model, k), v, f"Field {k} not matched for model {model}")


    def assertModelFunction(self, function, data):
        """
        Checks that the model returns the proper data for the function
        """
        for k, v in data.items():
            func = getattr(k, function)
            value = func()
            
            # Convert QuerySets to lists for comparison
            if isinstance(value, QuerySet):
                value = list(value)    
            
            self.assertEqual(value, v, f"Function {function} returned improper value for model {k}")