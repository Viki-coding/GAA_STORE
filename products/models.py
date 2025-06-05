from django.db import models


# Base Product model - concrete (not abstract)
class Product(models.Model):
    """
    Represents a generic product in the store.
    This is the base model for specific product types like Hurley, Grip,
    Sliotar, and Helmet.
    """
    name = models.CharField(max_length=50, help_text="Name of the product.")
    description = models.TextField(
        help_text="Detailed description of the product.")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price of the produfct."
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        default='products/default-product.jpg',
        help_text="Image of the product."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the product was created."
    )

    def __str__(self):
        """
        Returns the string representation of the product.
        """
        return self.name

    def get_specific_instance(self):
        """
        Returns the specific product type instance
        (e.g., Hurley, Grip, Sliotar, Helmet).
        If no specific type is associated, returns the base Product instance.
        """
        if hasattr(self, 'hurley'):
            return self.hurley
        elif hasattr(self, 'grip'):
            return self.grip
        elif hasattr(self, 'sliotar'):
            return self.sliotar
        elif hasattr(self, 'helmet'):
            return self.helmet
        return self


class Manufacturer(models.Model):
    """
    Represents a manufacturer of hurleys.
    """
    name = models.CharField(
        max_length=50, help_text="Name of the manufacturer.")
    description = models.TextField(
        help_text="Short description of the manufacturer.")

    def __str__(self):
        return self.name


# Specific product models (with one-to-one relationships to Product)
class Hurley(models.Model):
    """
    Represents a Hurley product with specific attributes like grip color,
    weight, and size.
    """
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True,
        related_name='hurley',
        help_text="The base product associated with this Hurley."
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE,
        help_text="Manufacturer of the Hurley.",
    )
    grip_color = models.CharField(
        max_length=20,
        choices=[
            ('black', 'Black'),
            ('red', 'Red'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('white', 'White'),
            ('pink', 'Pink'),
            ('orange', 'Orange'),
            ('yellow', 'Yellow'),
        ],
        default='black',
        help_text="Color of the grip on the Hurley."
    )
    weight = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Light'),
            ('medium', 'Medium'),
            ('heavy', 'Heavy'),
        ],
        default='medium',
        help_text="Weight category of the Hurley."
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ('20 inch', '20 inch'),
            ('22 inch', '22 inch'),
            ('24 inch', '24 inch'),
            ('25 inch', '25 inch'),
            ('26 inch', '26 inch'),
            ('27 inch', '27 inch'),
            ('28 inch', '28 inch'),
            ('29 inch', '29 inch'),
            ('30 inch', '30 inch'),
            ('31 inch', '31 inch'),
            ('32 inch', '32 inch'),
            ('33 inch', '33 inch'),
            ('34 inch', '34 inch'),
            ('35 inch', '35 inch'),
            ('36 inch', '36 inch'),
            ('37 inch', '37 inch'),
        ],
        help_text="Size of the Hurley in inches."
    )
    type = models.CharField(
        max_length=20,
        choices=[
            ('ash', 'Ash'),
            ('bambu', 'Bambú'),
            ('goalie', 'Goalie'),
        ],
        default='ash',
        help_text="Type of the Hurley."
    )

    def __str__(self):
        """
        Returns the string representation of the Hurley, including its size
        and grip color.
        """
        return f"{self.product.name} - {self.size}, {self.grip_color}, {
            self.manufacturer}"


class Grip(models.Model):
    """
    Represents a Grip product with a specific color.
    """
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True,
        help_text="The base product associated with this Grip."
    )
    color = models.CharField(
        max_length=20,
        choices=[
            ('black', 'Black'),
            ('red', 'Red'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('white', 'White'),
            ('pink', 'Pink'),
            ('orange', 'Orange'),
            ('yellow', 'Yellow'),
        ],
        help_text="Color of the grip."
    )

    def __str__(self):
        return f"{self.product.name} - Grip Color: {self.color}"

        class Meta:
            verbose_name = "Hurley"
            verbose_name_plural = "Hurleys"


class Sliotar(models.Model):
    """
    Represents a Sliotar product with a specific color.
    """
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True,
        help_text="The base product associated with this Sliotar."
    )
    color = models.CharField(
        max_length=20,
        choices=[
            ('white', 'White'),
            ('yellow', 'Yellow'),
        ],
        help_text="Color of the Sliotar."
    )

    def __str__(self):
        """
        Returns the string representation of the Sliotar, including its color.
        """
        return f"{self.product.name} - {self.color}"


class Helmet(models.Model):
    """
    Represents a Helmet product with specific attributes like color and size.
    """
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True,
        help_text="The base product associated with this Helmet."
    )
    color = models.CharField(
        max_length=20,
        choices=[
            ('black', 'Black'),
            ('red', 'Red'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('pink', 'Pink'),
        ],
        help_text="Color of the helmet."
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
        ],
        help_text="Size of the helmet."
    )

    def __str__(self):
        """
        Returns the string representation of the Helmet, including its
        size and color.
        """
        return f"{self.product.name} - {self.size}, {self.color}"
