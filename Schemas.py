from marshmallow import Schema, fields, validate, validates, ValidationError 



class UserLoginSchema(Schema):
    handler = fields.Str(required=False, validate=validate.Length(
        min=1, error="This field cannot be empty"))
    password = fields.Str(required=True, load_only=True)

    @validates('password')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError(" Password field cannot be empty.")


class AdminRetrival(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    Email = fields.Str(required=True)
    Role = fields.Str(required=False)


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)  # appear only in response
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    Email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Email input should be of type Email. Example: Name@something.com"
        }
    )
    password = fields.Str(required=True,
                        load_only=True,
                        validate=validate.Length(min=8, 
                                                 error="Password must be at least 8 characters long."))
    phone = fields.Str(required=True,
                       validate=validate.Length(equal=11, 
                                                 error="Phone number must be 11 digit."))
    user_type = fields.Str(required=True)
    profile_pic= fields.Str(dump_only=True)
    @validates('password')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError(" Password field cannot be empty.")

# class ClientLocationSchema(Schema):
#     id = fields.Int(dump_only=True)
#     city = fields.Str(required=True)
#     district = fields.Str(required=True)
#     building = fields.Str(required=True)
#     street = fields.Str(required=True)
#     floor = fields.Str(required=True)
#     apartment = fields.Str(required=True)
#     additional = fields.Str(required=True)
#     long = fields.Str(required=True)
#     lat = fields.Str(required=True)


class CraftsmanSchema(Schema):
    id = fields.Int(dump_only=True)  # appear only in response
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    phone = fields.Str(required=True)
    user_type = fields.Str(required=True)
    category_name = fields.Str(required=True)
    pending = fields.Str(dump_only=True)
    profile_pic=fields.Str(dump_only=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(
            min=8, error="Password must be at least 8 characters long.")
    )
    Email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Email input should be of type Email. Example: Name@something.com"
        }
    )

class CraftsmanReview(Schema):
        client_id = fields.Int()
        Client_name=fields.Str()
        craftsman_name=fields.Str()
        rating = fields.Float()
        feedback = fields.String()
        name=fields.Str()

class RequestedCraftsman(Schema):
        id = fields.Int(dump_only=True)  # appear only in response
        name = fields.Str(required=True)
        username = fields.Str(required=True)
        phone = fields.Str(required=True)
        profile_pic=fields.Str(dump_only=True)
        completed_orders=fields.Int()
        rating= fields.Str(dump_only=True)
        fare=fields.Str()



class serialzed(Schema):
    rate=fields.Int(required=True)
class PendingCraftsmenSchema(CraftsmanSchema):
    front_image= fields.Str(required=True)
    back_image= fields.Str(required=True)


# ********************************************************************************************************


# Admin set new locations
class SetlocationSchema(Schema):
    id = fields.Int(dump_only=True)
    locations = fields.List(fields.Str(), required=True)


class ReturnlocationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class PlainAddCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    details = fields.Str(required=True)


class PlainAddStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    description=fields.Str()
    phone=fields.Str()


class PlainAddItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Str(required=True)
    quantity = fields.Int(required=True)
    image = fields.Str(dump_only=True)
    store_name = fields.Str(required=True)


class ItemsInStoreSchema(PlainAddItemSchema):
    stores = fields.Nested(PlainAddStoreSchema)


class SpeceficItemSchema(Schema):
    name = fields.Str(required=True)


class ReturnSpeceficItemSchema(SpeceficItemSchema):
    stores = fields.Nested(PlainAddStoreSchema())


class AddcategorySchema(PlainAddCategorySchema):
    category = fields.List(fields.Nested(
        PlainAddCategorySchema), dump_only=True)


class AddServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(
        min=1, max=255, error="This field cannot be empty"))
    price = fields.Int(required=True, allow_none=False)
    category = fields.Str(required=True, allow_none=False)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("field cannot be empty.")


class PlainMessageSchema(Schema):
    id = fields.Int(dump_only=True)
    ContactEmail = fields.Str(required=True)
    MessageDetail = fields.Str(required=True)
    user_type = fields.Str(required=True)
    user_id = fields.Int(required=True)
    @validates('MessageDetail')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("field cannot be empty.")

class MessageSchema(Schema):
    id = fields.Int(load_only=True)
    ContactEmail = fields.Str(required=True)
    MessageDetail = fields.Str(required=True)
    @validates('MessageDetail')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("field cannot be empty.")

    

class MailSchema(Schema):
    cratftsman_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    body = fields.Str(required=True)
    @validates('body')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("field cannot be empty.")


    # @validates('body')
    # def validate_name(self, value):
    #     if not value.strip():
    #         raise ValidationError("Mail body cannot be empty.")


class CraftsmanCategorySchema(CraftsmanSchema):
    category_name = fields.Nested(PlainAddCategorySchema)


class CouponSchema(Schema):
    store_id = fields.Int(dump_only=True)
    code = fields.String()
    value = fields.Integer(format="%")
    date_created = fields.Date(format="%d/%m/%Y")
    exp_date = fields.Date(format="%d/%m/%Y")


class PlainServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    price = fields.Int()

class Category(Schema):
    name = fields.Str(required=True)


class ServicesWithCategory(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Integer()

    category = fields.Nested(Category)

class NestedServiceSchema(Schema):
    services = fields.List(fields.Nested(PlainServiceSchema))



class ServiceListSchema(Schema):
    services = fields.List(fields.Str(), required=True)
    date=fields.DateTime()
    area= fields.Str(required=True)
    additional=fields.Str()
class FilteredCraftsmen(Schema):
    order_id=fields.Integer()
class orderServices(Schema):
    service_id=fields.Integer()
class orderSchema(Schema):
    order_id=fields.Integer()
    client_id=fields.Str()
    craftsman_id=fields.Str()
    done=fields.Bool()
    total=fields.Int()
    date=fields.DateTime()
    Client_name=fields.Str()
    craftsman_name=fields.Str()
    area=fields.Str()
    additional=fields.Str()
    services = fields.List(fields.Nested(PlainServiceSchema), attribute="order_services")

class nestedorder(orderSchema):
    services = fields.List(fields.Nested(NestedServiceSchema))
class OrderServicesSchema(Schema):#new
    service = fields.Nested(PlainServiceSchema)


class NewOrderSchema(Schema):
    order_id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    craftsman_id = fields.Int(allow_none=True)
    Client_name=fields.Str()
    craftsman_name=fields.Str()
    done = fields.Bool(required=True)
    total=fields.Int(required=True)
    date=fields.DateTime()
    area=fields.Str()
    additional=fields.Str()
    services = fields.List(fields.Nested(PlainServiceSchema), attribute="order_services")



class OrderServicesOnlySchema(Schema):
    services = fields.List(fields.Nested(PlainServiceSchema), attribute="order_services")

class CloseRequestSchema(Schema):
    # order_id = fields.Int(dump_only=True)
    rate=fields.Int(required=True)
    feedback=fields.Str()
    
class walletSchema(Schema):
    id = fields.Int(dump_only=True)
    balance = fields.Float()
    craftsman_id = fields.Int()
class paymentSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    total=fields.Int()


